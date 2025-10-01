from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count, Avg
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import csv

@login_required
def financial_reports(request):
    """Comprehensive financial reports and analytics"""
    
    # Get date range from request or use default (last 30 days)
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
    
    # Custom date range
    custom_start = request.GET.get('start_date')
    custom_end = request.GET.get('end_date')
    if custom_start:
        start_date = datetime.strptime(custom_start, '%Y-%m-%d')
    if custom_end:
        end_date = datetime.strptime(custom_end, '%Y-%m-%d')
    
    # Import models here to avoid circular imports
    from .models import Client, Payment, Invoice, ServicePlan
    
    # Calculate key financial metrics
    period_revenue = Payment.objects.filter(
        payment_date__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Revenue by payment method
    revenue_by_method = Payment.objects.filter(
        payment_date__range=[start_date, end_date]
    ).values('payment_method').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Active clients and ARPU
    active_clients = Client.objects.filter(is_active=True).count()
    arpu = period_revenue / active_clients if active_clients > 0 else Decimal('0')
    
    # Invoice aging
    current_date = timezone.now().date()
    invoice_aging = {
        'current': Invoice.objects.filter(due_date__gte=current_date, status='pending').aggregate(total=Sum('amount'))['total'] or Decimal('0'),
        '1_30_days': Invoice.objects.filter(
            due_date__lt=current_date,
            due_date__gte=current_date - timedelta(days=30),
            status='pending'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0'),
        'over_30_days': Invoice.objects.filter(
            due_date__lt=current_date - timedelta(days=30),
            status='pending'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0'),
    }
    
    # Collection rate
    total_invoiced = Invoice.objects.filter(
        created_at__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    collection_rate = (period_revenue / total_invoiced * 100) if total_invoiced > 0 else Decimal('0')
    
    # Service plan performance
    plan_performance = []
    for plan in ServicePlan.objects.all():
        plan_clients = Client.objects.filter(service_plan=plan, is_active=True).count()
        plan_revenue = Payment.objects.filter(
            client__service_plan=plan,
            payment_date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        if plan_clients > 0:
            avg_revenue = plan_revenue / plan_clients
            plan_performance.append({
                'name': plan.name,
                'clients': plan_clients,
                'revenue': plan_revenue,
                'avg_revenue': avg_revenue,
                'price': plan.price
            })
    
    context = {
        'start_date': start_date.date(),
        'end_date': end_date.date(),
        'period': period,
        'period_revenue': period_revenue,
        'revenue_by_method': list(revenue_by_method),
        'active_clients': active_clients,
        'arpu': arpu,
        'invoice_aging': invoice_aging,
        'collection_rate': collection_rate,
        'plan_performance': plan_performance,
        'total_invoiced': total_invoiced,
    }
    
    return render(request, 'clients/financial_reports.html', context)

@login_required
def financial_reports_api(request):
    """API endpoint for financial data"""
    period = request.GET.get('period', 'monthly')
    end_date = timezone.now()
    
    if period == 'monthly':
        start_date = end_date - timedelta(days=30)
    else:
        start_date = end_date - timedelta(days=365)
    
    from .models import Payment
    
    # Revenue by day for charts
    revenue_by_day = Payment.objects.filter(
        payment_date__range=[start_date, end_date]
    ).extra({'date': "date(payment_date)"}).values('date').annotate(
        total=Sum('amount')
    ).order_by('date')
    
    data = {
        'revenue_by_day': list(revenue_by_day),
        'period': period
    }
    
    return JsonResponse(data)

@login_required
def export_financial_report(request):
    """Export financial report to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financial_report.csv"'
    
    writer = csv.writer(response)
    
    # Get basic financial data
    from .models import Client, Payment, Invoice
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    period_revenue = Payment.objects.filter(
        payment_date__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Write CSV
    writer.writerow(['Financial Report', f'Period: {start_date.date()} to {end_date.date()}'])
    writer.writerow([])
    writer.writerow(['Metric', 'Value'])
    writer.writerow(['Total Revenue', f'KSh {period_revenue:,.2f}'])
    writer.writerow(['Active Clients', Client.objects.filter(is_active=True).count()])
    writer.writerow(['Pending Invoices', Invoice.objects.filter(status='pending').count()])
    writer.writerow(['Collection Rate', f'{(period_revenue / Invoice.objects.filter(created_at__range=[start_date, end_date]).aggregate(total=Sum("amount"))["total"] * 100) if Invoice.objects.filter(created_at__range=[start_date, end_date]).exists() else 0:.1f}%'])
    
    return response
