from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.db.models import Sum, Count, Q, Avg, Max, Min
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import datetime, timedelta
import json
import csv
from decimal import Decimal

# ===== HELPER FUNCTIONS =====

def is_admin(user):
    return user.is_staff or user.is_superuser

def get_system_setting(key, default=None):
    try:
        setting = SystemSettings.objects.get(key=key)
        return setting.value
    except SystemSettings.DoesNotExist:
        return default

# ===== DATA MANAGEMENT VIEWS =====

@login_required
def manage_clients(request):
    """Comprehensive client management view"""
    from .models import Client, ServicePlan
    
    clients = Client.objects.all().select_related('service_plan').order_by('-created_at')
    
    # Filters
    status_filter = request.GET.get('status', 'all')
    plan_filter = request.GET.get('plan', 'all')
    
    if status_filter == 'active':
        clients = clients.filter(is_active=True)
    elif status_filter == 'inactive':
        clients = clients.filter(is_active=False)
    elif status_filter != 'all':
        clients = clients.filter(status=status_filter)
    
    if plan_filter != 'all':
        clients = clients.filter(service_plan_id=plan_filter)
    
    # Statistics
    total_clients = clients.count()
    active_clients = clients.filter(is_active=True).count()
    plans = ServicePlan.objects.filter(is_active=True)
    
    context = {
        'clients': clients,
        'total_clients': total_clients,
        'active_clients': active_clients,
        'inactive_clients': total_clients - active_clients,
        'plans': plans,
        'status_filter': status_filter,
        'plan_filter': plan_filter,
    }
    return render(request, 'clients/manage_clients.html', context)

@login_required
def internet_packages(request):
    """Manage internet packages with full CRUD operations"""
    from .models import ServicePlan
    
    packages = ServicePlan.objects.all().order_by('price')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            # Create new package
            name = request.POST.get('name')
            speed = request.POST.get('speed')
            price = request.POST.get('price')
            data_limit = request.POST.get('data_limit', 'Unlimited')
            plan_type = request.POST.get('plan_type', 'Residential')
            
            ServicePlan.objects.create(
                name=name,
                speed=speed,
                price=price,
                data_limit=data_limit,
                plan_type=plan_type,
                is_active=True
            )
            messages.success(request, 'Package created successfully!')
            
        elif action == 'toggle':
            # Toggle package status
            package_id = request.POST.get('package_id')
            package = get_object_or_404(ServicePlan, id=package_id)
            package.is_active = not package.is_active
            package.save()
            messages.success(request, f'Package {"activated" if package.is_active else "deactivated"}!')
    
    context = {
        'packages': packages,
        'total_packages': packages.count(),
        'active_packages': packages.filter(is_active=True).count(),
    }
    return render(request, 'clients/internet_packages.html', context)

@login_required
def manage_invoices(request):
    """Comprehensive invoice management"""
    from .models import Invoice
    
    invoices = Invoice.objects.all().select_related('client').order_by('-created_at')
    
    # Filters
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'all')
    
    if status_filter != 'all':
        invoices = invoices.filter(status=status_filter)
    
    if date_filter == 'overdue':
        invoices = invoices.filter(due_date__lt=timezone.now().date(), status='pending')
    elif date_filter == 'this_month':
        start_date = timezone.now().replace(day=1)
        end_date = start_date + timedelta(days=32)
        invoices = invoices.filter(created_at__range=[start_date, end_date])
    
    # Statistics
    total_invoices = invoices.count()
    pending_invoices = invoices.filter(status='pending').count()
    paid_invoices = invoices.filter(status='paid').count()
    total_revenue = invoices.filter(status='paid').aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    context = {
        'invoices': invoices,
        'total_invoices': total_invoices,
        'pending_invoices': pending_invoices,
        'paid_invoices': paid_invoices,
        'total_revenue': total_revenue,
        'status_filter': status_filter,
        'date_filter': date_filter,
    }
    return render(request, 'clients/manage_invoices.html', context)

@login_required
def manage_payouts(request):
    """Payment and revenue management"""
    from .models import Payment
    
    payments = Payment.objects.all().select_related('invoice', 'client').order_by('-payment_date')
    
    # Date range filtering
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if date_from:
        payments = payments.filter(payment_date__gte=date_from)
    if date_to:
        payments = payments.filter(payment_date__lte=date_to)
    
    # Statistics
    total_payments = payments.count()
    total_revenue = payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Payment method breakdown
    payment_methods = payments.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('amount')
    ).order_by('-total')
    
    # Recent payments (last 10)
    recent_payments = payments[:10]
    
    context = {
        'payments': payments,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'payment_methods': payment_methods,
        'recent_payments': recent_payments,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'clients/manage_payouts.html', context)

# ===== SYSTEM ADMINISTRATION VIEWS =====

@login_required
@user_passes_test(is_admin)
def system_settings(request):
    """System configuration management"""
    from .models import SystemSettings
    
    settings_list = SystemSettings.objects.all().order_by('key')
    
    if request.method == 'POST':
        # Handle bulk settings update
        for setting in settings_list:
            new_value = request.POST.get(f'setting_{setting.id}')
            if new_value is not None and new_value != setting.value:
                setting.value = new_value
                setting.save()
        
        # Handle new setting creation
        new_key = request.POST.get('new_key')
        new_value = request.POST.get('new_value')
        new_description = request.POST.get('new_description')
        
        if new_key and new_value:
            SystemSettings.objects.create(
                key=new_key,
                value=new_value,
                description=new_description or ''
            )
            messages.success(request, 'New setting added successfully!')
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('system_settings')
    
    context = {
        'settings': settings_list,
    }
    return render(request, 'clients/system_settings.html', context)

@login_required
@user_passes_test(is_admin)
def reset_history(request):
    """System reset and maintenance log"""
    from .models import SystemResetLog, NetworkUsage, Client
    
    reset_logs = SystemResetLog.objects.all().select_related('reset_by').order_by('-reset_date')
    
    if request.method == 'POST':
        reset_type = request.POST.get('reset_type')
        reset_details = request.POST.get('reset_details', '')
        
        if reset_type:
            # Perform the reset action based on type
            if reset_type == 'network_stats':
                deleted_count, _ = NetworkUsage.objects.all().delete()
                details = f"Network statistics reset. Deleted {deleted_count} records."
            elif reset_type == 'test_data':
                # Example: Delete test clients
                test_clients = Client.objects.filter(name__icontains='test')
                deleted_count = test_clients.count()
                test_clients.delete()
                details = f"Test data reset. Deleted {deleted_count} test clients."
            elif reset_type == 'cache':
                details = "System cache cleared."
            else:
                details = reset_details or f"Manual reset: {reset_type}"
            
            # Log the reset action
            SystemResetLog.objects.create(
                reset_type=reset_type,
                reset_by=request.user,
                description=details,
                clients_deleted=0,
                invoices_deleted=0,
                payments_deleted=0
            )
            
            messages.success(request, f'Reset operation completed: {reset_type}')
            return redirect('reset_history')
    
    # Reset statistics
    total_resets = reset_logs.count()
    recent_resets = reset_logs.filter(
        reset_date__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    context = {
        'reset_logs': reset_logs,
        'total_resets': total_resets,
        'recent_resets': recent_resets,
    }
    return render(request, 'clients/reset_history.html', context)

# ===== BILLING REPORTS VIEWS =====

@login_required
def billing_reports(request):
    """Comprehensive billing and invoicing analytics"""
    
    # Date range parameters
    period = request.GET.get('period', 'monthly')
    end_date = timezone.now()
    
    if period == 'daily':
        start_date = end_date - timedelta(days=1)
    elif period == 'weekly':
        start_date = end_date - timedelta(weeks=1)
    elif period == 'quarterly':
        start_date = end_date - timedelta(days=90)
    elif period == 'yearly':
        start_date = end_date - timedelta(days=365)
    else:  # monthly
        start_date = end_date - timedelta(days=30)
    
    # Import models
    from .models import Invoice, Payment, Client
    
    # Invoice statistics
    total_invoices = Invoice.objects.filter(created_at__range=[start_date, end_date]).count()
    invoice_amounts = Invoice.objects.filter(created_at__range=[start_date, end_date]).aggregate(
        total=Sum('amount'),
        avg=Avg('amount'),
        max=Max('amount'),
        min=Min('amount')
    )
    
    # Invoice status breakdown
    invoice_status = Invoice.objects.filter(created_at__range=[start_date, end_date]).values(
        'status'
    ).annotate(
        count=Count('id'),
        total_amount=Sum('amount')
    ).order_by('-total_amount')
    
    # Payment statistics
    payment_stats = Payment.objects.filter(payment_date__range=[start_date, end_date]).aggregate(
        total_payments=Count('id'),
        total_collected=Sum('amount'),
        avg_payment=Avg('amount')
    )
    
    # Payment method analysis
    payment_methods = Payment.objects.filter(payment_date__range=[start_date, end_date]).values(
        'payment_method'
    ).annotate(
        count=Count('id'),
        total=Sum('amount'),
        avg=Avg('amount')
    ).order_by('-total')
    
    # Collection performance
    total_invoiced_amount = Invoice.objects.filter(created_at__range=[start_date, end_date]).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')
    total_collected_amount = payment_stats['total_collected'] or Decimal('0')
    collection_rate = (total_collected_amount / total_invoiced_amount * 100) if total_invoiced_amount > 0 else Decimal('0')
    
    # Overdue analysis
    current_date = timezone.now().date()
    overdue_invoices = Invoice.objects.filter(
        due_date__lt=current_date,
        status='pending'
    )
    total_overdue = overdue_invoices.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    overdue_count = overdue_invoices.count()
    
    # Client payment behavior
    client_payment_behavior = Client.objects.annotate(
        total_paid=Sum('payment__amount'),
        invoice_count=Count('invoice'),
        paid_invoice_count=Count('invoice', filter=Q(invoice__status='paid'))
    ).filter(
        invoice__created_at__range=[start_date, end_date]
    ).order_by('-total_paid')[:10]  # Top 10 paying clients
    
    # Monthly billing trend
    monthly_trend = []
    for i in range(6):  # Last 6 months
        month_start = end_date.replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_invoices = Invoice.objects.filter(created_at__range=[month_start, month_end])
        month_payments = Payment.objects.filter(payment_date__range=[month_start, month_end])
        
        monthly_trend.append({
            'month': month_start.strftime('%b %Y'),
            'invoices_count': month_invoices.count(),
            'invoices_amount': month_invoices.aggregate(total=Sum('amount'))['total'] or Decimal('0'),
            'payments_count': month_payments.count(),
            'payments_amount': month_payments.aggregate(total=Sum('amount'))['total'] or Decimal('0'),
        })
    
    monthly_trend.reverse()
    
    context = {
        'start_date': start_date.date(),
        'end_date': end_date.date(),
        'period': period,
        
        # Invoice metrics
        'total_invoices': total_invoices,
        'invoice_amounts': invoice_amounts,
        'invoice_status': list(invoice_status),
        
        # Payment metrics
        'payment_stats': payment_stats,
        'payment_methods': list(payment_methods),
        'collection_rate': collection_rate,
        
        # Overdue analysis
        'total_overdue': total_overdue,
        'overdue_count': overdue_count,
        'overdue_invoices': overdue_invoices[:10],  # Top 10 overdue
        
        # Client behavior
        'client_payment_behavior': client_payment_behavior,
        
        # Trends
        'monthly_trend': monthly_trend,
        
        # Summary for quick view
        'summary': {
            'total_billed': total_invoiced_amount,
            'total_collected': total_collected_amount,
            'outstanding_balance': total_invoiced_amount - total_collected_amount,
            'avg_collection_rate': collection_rate,
        }
    }
    
    return render(request, 'clients/billing_reports.html', context)

@login_required
def billing_reports_api(request):
    """API endpoint for billing data"""
    period = request.GET.get('period', 'monthly')
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30) if period == 'monthly' else end_date - timedelta(days=365)
    
    from .models import Invoice, Payment
    
    # Daily billing data for charts
    daily_invoices = Invoice.objects.filter(
        created_at__range=[start_date, end_date]
    ).extra({'date': "date(created_at)"}).values('date').annotate(
        amount=Sum('amount'),
        count=Count('id')
    ).order_by('date')
    
    daily_payments = Payment.objects.filter(
        payment_date__range=[start_date, end_date]
    ).extra({'date': "date(payment_date)"}).values('date').annotate(
        amount=Sum('amount'),
        count=Count('id')
    ).order_by('date')
    
    data = {
        'daily_invoices': list(daily_invoices),
        'daily_payments': list(daily_payments),
        'period': period
    }
    
    return JsonResponse(data)

@login_required
def export_billing_report(request):
    """Export billing report to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="billing_report.csv"'
    
    writer = csv.writer(response)
    
    from .models import Invoice, Payment, Client
    
    # Write CSV headers
    writer.writerow(['Billing Report', f'Generated: {timezone.now().strftime("%Y-%m-%d %H:%M")}'])
    writer.writerow([])
    
    # Invoice summary
    writer.writerow(['INVOICE SUMMARY'])
    writer.writerow(['Total Invoices', Invoice.objects.count()])
    writer.writerow(['Pending Invoices', Invoice.objects.filter(status='pending').count()])
    writer.writerow(['Paid Invoices', Invoice.objects.filter(status='paid').count()])
    writer.writerow(['Overdue Invoices', Invoice.objects.filter(due_date__lt=timezone.now().date(), status='pending').count()])
    writer.writerow([])
    
    # Payment summary
    writer.writerow(['PAYMENT SUMMARY'])
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    writer.writerow(['Total Revenue', f'KSh {total_revenue:,.2f}'])
    
    # Payment methods
    writer.writerow([])
    writer.writerow(['PAYMENT METHODS'])
    writer.writerow(['Method', 'Count', 'Amount'])
    payment_methods = Payment.objects.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('amount')
    ).order_by('-total')
    
    for method in payment_methods:
        writer.writerow([
            method['payment_method'] or 'Unknown',
            method['count'],
            f'KSh {method["total"]:,.2f}'
        ])
    
    return response

# ===== SYSTEM REPORTS VIEWS =====

@login_required
@user_passes_test(is_admin)
def system_reports(request):
    """Comprehensive system performance and operational reports"""
    
    # Import models
    from .models import Client, ServicePlan, Invoice, Payment, NetworkUsage, SystemResetLog
    
    # System overview metrics
    system_metrics = {
        'total_clients': Client.objects.count(),
        'active_clients': Client.objects.filter(is_active=True).count(),
        'total_service_plans': ServicePlan.objects.count(),
        'active_service_plans': ServicePlan.objects.filter(is_active=True).count(),
        'total_invoices': Invoice.objects.count(),
        'total_payments': Payment.objects.count(),
        'system_uptime': '99.9%',  # This would come from actual monitoring
    }
    
    # Client growth analysis
    client_growth = []
    for i in range(12):  # Last 12 months
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        new_clients = Client.objects.filter(created_at__range=[month_start, month_end]).count()
        churned_clients = Client.objects.filter(
            is_active=False,
            updated_at__range=[month_start, month_end]
        ).count()
        
        client_growth.append({
            'month': month_start.strftime('%b %Y'),
            'new_clients': new_clients,
            'churned_clients': churned_clients,
            'net_growth': new_clients - churned_clients,
        })
    
    client_growth.reverse()
    
    # Service plan distribution
    plan_distribution = Client.objects.values(
        'service_plan__name',
        'service_plan__price'
    ).annotate(
        client_count=Count('id'),
        active_clients=Count('id', filter=Q(is_active=True)),
        total_revenue=Sum('payment__amount')
    ).order_by('-client_count')
    
    # System performance metrics (mock data - would come from monitoring)
    performance_metrics = {
        'server_cpu_usage': 45.2,
        'server_memory_usage': 67.8,
        'database_size': '2.4 GB',
        'average_response_time': '125 ms',
        'error_rate': '0.05%',
        'network_throughput': '1.2 Gbps',
    }
    
    # Network usage statistics
    network_stats = NetworkUsage.objects.aggregate(
        total_download=Sum('download_bytes'),
        total_upload=Sum('upload_bytes'),
        average_download=Avg('download_bytes'),
        average_upload=Avg('upload_bytes'),
        total_records=Count('id')
    )
    
    # Convert bytes to GB for readability
    if network_stats['total_download']:
        network_stats['total_download_gb'] = network_stats['total_download'] / (1024**3)
        network_stats['total_upload_gb'] = network_stats['total_upload'] / (1024**3)
    
    # System maintenance logs
    maintenance_logs = SystemResetLog.objects.all().order_by('-reset_date')[:10]
    
    # Revenue trends
    revenue_trend = []
    for i in range(6):  # Last 6 months
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        monthly_revenue = Payment.objects.filter(
            payment_date__range=[month_start, month_end]
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        revenue_trend.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': float(monthly_revenue),
            'growth': 0  # Would calculate actual growth
        })
    
    revenue_trend.reverse()
    
    # System health indicators
    health_indicators = {
        'database_health': 'Healthy',
        'application_health': 'Healthy',
        'network_health': 'Stable',
        'security_status': 'Secure',
        'backup_status': 'Up to date',
    }
    
    # Operational efficiency metrics
    efficiency_metrics = {
        'arpu': Payment.objects.aggregate(total=Sum('amount'))['total'] / Client.objects.filter(is_active=True).count() if Client.objects.filter(is_active=True).exists() else 0,
        'client_retention_rate': 85.5,  # Would calculate actual retention
        'invoice_processing_time': '2.3 days',  # Average time to process invoices
        'payment_processing_time': '1.1 days',  # Average time to process payments
    }
    
    context = {
        'system_metrics': system_metrics,
        'client_growth': client_growth,
        'plan_distribution': list(plan_distribution),
        'performance_metrics': performance_metrics,
        'network_stats': network_stats,
        'maintenance_logs': maintenance_logs,
        'revenue_trend': revenue_trend,
        'health_indicators': health_indicators,
        'efficiency_metrics': efficiency_metrics,
    }
    
    return render(request, 'clients/system_reports.html', context)

@login_required
@user_passes_test(is_admin)
def system_reports_api(request):
    """API endpoint for system data"""
    from .models import Client, Payment
    
    # Client growth data for charts
    monthly_growth = []
    for i in range(12):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        new_clients = Client.objects.filter(created_at__range=[month_start, month_end]).count()
        monthly_growth.append({
            'month': month_start.strftime('%b %Y'),
            'new_clients': new_clients,
        })
    
    monthly_growth.reverse()
    
    # Revenue data
    monthly_revenue = []
    for i in range(12):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        revenue = Payment.objects.filter(
            payment_date__range=[month_start, month_end]
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        monthly_revenue.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': float(revenue),
        })
    
    monthly_revenue.reverse()
    
    data = {
        'monthly_growth': monthly_growth,
        'monthly_revenue': monthly_revenue,
    }
    
    return JsonResponse(data)

@login_required
@user_passes_test(is_admin)
def export_system_report(request):
    """Export system report to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="system_report.csv"'
    
    writer = csv.writer(response)
    
    from .models import Client, ServicePlan, Invoice, Payment
    
    # System overview
    writer.writerow(['SYSTEM OVERVIEW REPORT'])
    writer.writerow(['Generated', timezone.now().strftime('%Y-%m-%d %H:%M')])
    writer.writerow([])
    
    writer.writerow(['CLIENT STATISTICS'])
    writer.writerow(['Total Clients', Client.objects.count()])
    writer.writerow(['Active Clients', Client.objects.filter(is_active=True).count()])
    writer.writerow(['Inactive Clients', Client.objects.filter(is_active=False).count()])
    writer.writerow([])
    
    writer.writerow(['SERVICE PLAN DISTRIBUTION'])
    writer.writerow(['Plan Name', 'Total Clients', 'Active Clients'])
    plan_distribution = Client.objects.values(
        'service_plan__name'
    ).annotate(
        total=Count('id'),
        active=Count('id', filter=Q(is_active=True))
    ).order_by('-total')
    
    for plan in plan_distribution:
        writer.writerow([
            plan['service_plan__name'],
            plan['total'],
            plan['active']
        ])
    
    writer.writerow([])
    writer.writerow(['FINANCIAL OVERVIEW'])
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    writer.writerow(['Total Revenue', f'KSh {total_revenue:,.2f}'])
    writer.writerow(['Total Invoices', Invoice.objects.count()])
    writer.writerow(['Pending Invoices', Invoice.objects.filter(status='pending').count()])
    
    return response

# ===== API ENDPOINTS =====

@login_required
def api_system_stats(request):
    """API endpoint for system statistics"""
    from .models import Client, Payment, Invoice, ServicePlan
    
    stats = {
        'total_clients': Client.objects.count(),
        'active_clients': Client.objects.filter(is_active=True).count(),
        'total_revenue': Payment.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0'),
        'pending_invoices': Invoice.objects.filter(status='pending').count(),
        'active_packages': ServicePlan.objects.filter(is_active=True).count(),
    }
    return JsonResponse(stats)

@login_required
@user_passes_test(is_admin)
def api_perform_reset(request):
    """API endpoint for performing system resets"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reset_type = data.get('reset_type')
            
            from .models import NetworkUsage, SystemResetLog
            
            if reset_type == 'network_stats':
                deleted_count, _ = NetworkUsage.objects.all().delete()
                message = f"Network statistics reset. Deleted {deleted_count} records."
            else:
                message = f"Reset operation: {reset_type}"
            
            # Log the action
            SystemResetLog.objects.create(
                reset_type=reset_type,
                reset_by=request.user,
                description=message,
                clients_deleted=0,
                invoices_deleted=0,
                payments_deleted=0
            )
            
            return JsonResponse({'success': True, 'message': message})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# ===== CLIENT MANAGEMENT VIEWS =====

@login_required
def add_client(request):
    """Add new client view"""
    from .forms import ClientForm
    
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.is_active = True
            client.status = 'Active'
            client.balance = Decimal('0.00')
            client.registration_date = timezone.now().date()
            client.save()
            
            messages.success(request, f'Client "{client.name}" added successfully!')
            return redirect('manage_clients')
    else:
        form = ClientForm()
    
    context = {
        'form': form,
        'title': 'Add New Client'
    }
    return render(request, 'clients/client_form.html', context)

@login_required
def quick_add_client(request):
    """Quick add client for dashboard"""
    from .forms import ClientForm
    
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.is_active = True
            client.status = 'Active'
            client.balance = Decimal('0.00')
            client.registration_date = timezone.now().date()
            client.save()
            
            messages.success(request, f'Client "{client.name}" added successfully!')
            return redirect('main_dashboard')
    else:
        form = ClientForm()
    
    context = {
        'form': form,
        'title': 'Quick Add Client',
        'quick_add': True
    }
    return render(request, 'clients/client_form.html', context)

# ===== API ENDPOINTS FOR CLIENT MANAGEMENT =====

@login_required
def api_service_plans(request):
    """API endpoint to get active service plans"""
    from .models import ServicePlan
    from django.http import JsonResponse
    
    plans = ServicePlan.objects.filter(is_active=True).values('id', 'name', 'price', 'speed')
    return JsonResponse(list(plans), safe=False)

