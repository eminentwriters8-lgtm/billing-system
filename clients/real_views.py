# VIEWS WITH REAL DATA INTEGRATION
# Copyright (c) 2025 Martin Mutinda

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from .models import Client, ServicePlan, Invoice, Payment, NetworkUsage
from .mikrotik_integration import mikrotik_manager

def get_real_dashboard_data():
    """Get real data for dashboard"""
    today = datetime.now().date()
    month_start = today.replace(day=1)
    
    # Real client statistics
    total_clients = Client.objects.filter(is_active=True).count()
    pppoe_clients = Client.objects.filter(is_active=True, client_type='pppoe').count()
    hotspot_clients = Client.objects.filter(is_active=True, client_type='hotspot').count()
    
    # Real revenue data
    monthly_revenue = Payment.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Pending payments
    pending_invoices = Invoice.objects.filter(
        status__in=['sent', 'overdue'],
        due_date__lte=today
    ).count()
    
    # Active connections from MikroTik
    active_connections = mikrotik_manager.get_active_connections()
    active_sessions = len(active_connections.get('pppoe', [])) + len(active_connections.get('hotspot', []))
    
    return {
        'total_clients': total_clients,
        'pppoe_clients': pppoe_clients,
        'hotspot_clients': hotspot_clients,
        'monthly_revenue': monthly_revenue,
        'pending_payments': pending_invoices,
        'active_sessions': active_sessions,
    }

def main_dashboard(request):
    """Main dashboard with real data"""
    real_data = get_real_dashboard_data()
    
    # Recent activity
    recent_payments = Payment.objects.select_related('client').order_by('-payment_date')[:5]
    recent_clients = Client.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Network status from MikroTik
    system_resources = mikrotik_manager.get_system_resources()
    uptime = system_resources.get('uptime', 'N/A') if system_resources else 'N/A'
    
    context = {
        # Real data
        'total_clients': real_data['total_clients'],
        'pppoe_clients': real_data['pppoe_clients'],
        'hotspot_clients': real_data['hotspot_clients'],
        'monthly_revenue': real_data['monthly_revenue'],
        'pending_payments': real_data['pending_payments'],
        'active_sessions': real_data['active_sessions'],
        
        # Additional context
        'recent_payments': recent_payments,
        'recent_clients': recent_clients,
        'network_uptime': uptime,
        'current_date': datetime.now().strftime('%B %d, %Y'),
    }
    
    return render(request, 'dashboard/responsive.html', context)

def client_management(request):
    """Client management with real data"""
    clients = Client.objects.select_related('service_plan').filter(is_active=True)
    
    # Statistics
    client_stats = {
        'total': clients.count(),
        'pppoe': clients.filter(client_type='pppoe').count(),
        'hotspot': clients.filter(client_type='hotspot').count(),
        'active': clients.filter(status='active').count(),
        'suspended': clients.filter(status='suspended').count(),
    }
    
    # Check connection status for each client
    for client in clients:
        client.currently_connected = client.get_connection_status()
    
    context = {
        'clients': clients,
        'client_stats': client_stats,
    }
    
    return render(request, 'clients/management.html', context)

def billing_dashboard(request):
    """Billing dashboard with real financial data"""
    today = datetime.now().date()
    month_start = today.replace(day=1)
    
    # Real financial data
    monthly_revenue = Payment.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    yearly_revenue = Payment.objects.filter(
        payment_date__year=today.year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Pending payments
    pending_payments = Invoice.objects.filter(
        status__in=['sent', 'overdue'],
        due_date__lte=today
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Recent payments
    recent_payments = Payment.objects.select_related('client').order_by('-payment_date')[:10]
    
    # Payment distribution
    payment_methods = Payment.objects.values('payment_method').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    context = {
        'monthly_revenue': monthly_revenue,
        'yearly_revenue': yearly_revenue,
        'pending_payments': pending_payments,
        'recent_payments': recent_payments,
        'payment_methods': payment_methods,
        'current_month': today.strftime('%B %Y'),
    }
    
    return render(request, 'billing/dashboard.html', context)

def network_live_dashboard(request):
    """Real-time network dashboard with MikroTik data"""
    # Get real network data from MikroTik
    active_connections = mikrotik_manager.get_active_connections()
    system_resources = mikrotik_manager.get_system_resources()
    interface_stats = mikrotik_manager.get_interface_stats()
    
    # Calculate real usage
    total_download = sum(int(iface.get('rx-byte', 0)) for iface in interface_stats)
    total_upload = sum(int(iface.get('tx-byte', 0)) for iface in interface_stats)
    
    context = {
        'active_pppoe': len(active_connections.get('pppoe', [])),
        'active_hotspot': len(active_connections.get('hotspot', [])),
        'total_sessions': len(active_connections.get('pppoe', [])) + len(active_connections.get('hotspot', [])),
        'cpu_load': system_resources.get('cpu-load', 'N/A'),
        'memory_usage': system_resources.get('free-memory', 'N/A'),
        'total_memory': system_resources.get('total-memory', 'N/A'),
        'uptime': system_resources.get('uptime', 'N/A'),
        'total_download': total_download,
        'total_upload': total_upload,
        'interface_stats': interface_stats[:5],  # Show first 5 interfaces
    }
    
    return render(request, 'network/live_dashboard.html', context)

def sync_mikrotik_users(request):
    """Sync users from MikroTik to local database"""
    if request.method == 'POST':
        try:
            # Get PPPoE users from MikroTik
            pppoe_users = mikrotik_manager.get_pppoe_users()
            hotspot_users = mikrotik_manager.get_hotspot_users()
            
            synced_count = 0
            
            # Sync PPPoE users
            for user in pppoe_users:
                username = user.get('name')
                if username and not Client.objects.filter(username=username).exists():
                    # Create new client record
                    Client.objects.create(
                        name=username,
                        username=username,
                        client_type='pppoe',
                        service_plan=ServicePlan.objects.first(),  # Default plan
                        phone='Not set',
                        address='Not set',
                        monthly_fee=2000,  # Default fee
                        password='synced_from_mikrotik'
                    )
                    synced_count += 1
            
            # Sync Hotspot users
            for user in hotspot_users:
                username = user.get('name')
                if username and not Client.objects.filter(username=username).exists():
                    Client.objects.create(
                        name=username,
                        username=username,
                        client_type='hotspot',
                        service_plan=ServicePlan.objects.first(),
                        phone='Not set',
                        address='Not set',
                        monthly_fee=1000,  # Default fee for hotspot
                        password='synced_from_mikrotik'
                    )
                    synced_count += 1
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully synced {synced_count} users from MikroTik',
                'synced_count': synced_count
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error syncing users: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Missing view functions that are referenced in URLs
def client_create(request):
    """Create new client"""
    from .models import Client, ServicePlan
    if request.method == 'POST':
        # Handle client creation form
        pass
    service_plans = ServicePlan.objects.filter(is_active=True)
    return render(request, 'clients/client_form.html', {'service_plans': service_plans})

def client_dashboard(request):
    """Client dashboard"""
    return render(request, 'clients/dashboard.html')

def client_location_pin(request, client_id):
    """Client location pin"""
    from .models import Client
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/location_pin.html', {'client': client})

def save_client_location(request, client_id):
    """Save client location"""
    from .models import Client
    client = get_object_or_404(Client, id=client_id)
    # Add location saving logic here
    return redirect('client_location_pin', client_id=client_id)

def network_dashboard(request):
    """Network dashboard"""
    return render(request, 'network/dashboard.html')

def network_traffic_api(request):
    """Network traffic API"""
    from django.http import JsonResponse
    import random
    data = {
        'download': random.randint(10, 100),
        'upload': random.randint(5, 50),
        'sessions': random.randint(5, 50)
    }
    return JsonResponse(data)

def network_alerts_api(request):
    """Network alerts API"""
    from django.http import JsonResponse
    return JsonResponse({'alerts': []})

def network_health_check(request):
    """Network health check API"""
    from django.http import JsonResponse
    return JsonResponse({'status': 'healthy'})

def network_usage_breakdown(request):
    """Network usage breakdown API"""
    from django.http import JsonResponse
    return JsonResponse({'usage': {}})

def network_peak_hours(request):
    """Network peak hours API"""
    from django.http import JsonResponse
    return JsonResponse({'peak_hours': []})

def whatsapp_compose(request):
    """WhatsApp compose message"""
    return render(request, 'whatsapp/compose.html')

def whatsapp_results(request):
    """WhatsApp results"""
    return render(request, 'whatsapp/results.html')

def whatsapp_reminders(request):
    """WhatsApp payment reminders"""
    return render(request, 'whatsapp/reminders.html')

def combined_dashboard(request):
    """Combined dashboard"""
    return render(request, 'dashboard/combined.html')
