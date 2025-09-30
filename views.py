# views.py
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count, Q, F
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Client, Payment, ServicePlan, DataUsage

def admin_dashboard(request):
    # Existing calculations
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(status='active').count()
    suspended_clients = Client.objects.filter(status='suspended').count()
    
    # Monthly revenue (existing)
    current_month = timezone.now().month
    monthly_revenue = Payment.objects.filter(
        payment_date__month=current_month,
        status='Completed'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Service stats (existing)
    service_stats = ServicePlan.objects.annotate(
        count=Count('client'),
        revenue=Sum('price')
    ).values('service_type', 'count', 'revenue')
    
    # Alert panels (existing)
    today = timezone.now().date()
    overdue_clients = Client.objects.filter(
        next_billing_date__lt=today,
        status='active'
    )
    expiring_soon = Client.objects.filter(
        next_billing_date__range=[today, today + timedelta(days=7)],
        status='active'
    )
    
    # Recent payments (existing)
    recent_payments = Payment.objects.select_related('client').order_by('-payment_date')[:5]
    
    # Monthly trend (existing)
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_trend = Payment.objects.filter(
        payment_date__gte=six_months_ago,
        status='Completed'
    ).extra({
        'month': "strftime('%%Y-%%m', payment_date)"
    }).values('month').annotate(
        revenue=Sum('amount')
    ).order_by('month')
    
    # NEW: Yearly Revenue with Quarterly Breakdown
    current_year = timezone.now().year
    yearly_payments = Payment.objects.filter(
        payment_date__year=current_year,
        status='Completed'
    )
    
    # Quarterly breakdown
    q1_revenue = yearly_payments.filter(
        payment_date__month__in=[1, 2, 3]
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    q2_revenue = yearly_payments.filter(
        payment_date__month__in=[4, 5, 6]
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    q3_revenue = yearly_payments.filter(
        payment_date__month__in=[7, 8, 9]
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    q4_revenue = yearly_payments.filter(
        payment_date__month__in=[10, 11, 12]
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    yearly_revenue = {
        'total': q1_revenue + q2_revenue + q3_revenue + q4_revenue,
        'q1': q1_revenue,
        'q2': q2_revenue,
        'q3': q3_revenue,
        'q4': q4_revenue
    }
    
    # NEW: Quarter-over-Quarter Growth Analysis
    quarterly_growth = []
    quarters = [
        ('Q1', q1_revenue),
        ('Q2', q2_revenue),
        ('Q3', q3_revenue),
        ('Q4', q4_revenue)
    ]
    
    for i, (quarter, revenue) in enumerate(quarters):
        if i == 0:
            growth = 0  # No previous quarter to compare with
        else:
            prev_revenue = quarters[i-1][1]
            if prev_revenue > 0:
                growth = ((revenue - prev_revenue) / prev_revenue) * 100
                growth = round(growth, 1)
            else:
                growth = 100 if revenue > 0 else 0
        
        quarterly_growth.append({
            'quarter': quarter,
            'revenue': revenue,
            'growth': growth
        })
    
    # NEW: Client Data Usage Tracking
    # Get top data users for the current month
    current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    top_data_users = DataUsage.objects.filter(
        usage_date__gte=current_month_start
    ).select_related('client', 'service_plan').values(
        'client__username',
        'service_plan__service_type',
        'data_used',
        'data_limit'
    ).annotate(
        client_name=F('client__username'),
        service_type=F('service_plan__service_type'),
        usage_percentage=(F('data_used') / F('data_limit')) * 100
    ).order_by('-data_used')[:10]
    
    # Convert usage_percentage to integer for template
    for user in top_data_users:
        user['usage_percentage'] = int(user['usage_percentage'])
    
    # NEW: Bandwidth Monitoring
    # Overall bandwidth stats (you might need to adjust this based on your infrastructure)
    total_bandwidth_capacity = 1000  # Example: 1000 GB total capacity
    used_bandwidth = DataUsage.objects.filter(
        usage_date__gte=current_month_start
    ).aggregate(Sum('data_used'))['data_used__sum'] or 0
    
    bandwidth_stats = {
        'total': total_bandwidth_capacity,
        'used': used_bandwidth,
        'usage_percentage': (used_bandwidth / total_bandwidth_capacity) * 100 if total_bandwidth_capacity > 0 else 0,
        'peak_morning': 45,  # Example data - replace with actual calculations
        'peak_afternoon': 65,  # Example data
        'peak_evening': 85,   # Example data
    }
    
    # NEW: Bandwidth Alerts
    bandwidth_alerts = []
    for user in top_data_users:
        if user['usage_percentage'] > 80:  # Alert if usage exceeds 80%
            bandwidth_alerts.append({
                'client_name': user['client_name'],
                'service_type': user['service_type'],
                'usage_percentage': user['usage_percentage'],
                'alert_type': 'high_usage' if user['usage_percentage'] <= 90 else 'critical_usage'
            })
    
    context = {
        # Existing context
        'total_clients': total_clients,
        'active_clients': active_clients,
        'suspended_clients': suspended_clients,
        'monthly_revenue': monthly_revenue,
        'service_stats': service_stats,
        'overdue_clients': overdue_clients,
        'expiring_soon': expiring_soon,
        'recent_payments': recent_payments,
        'monthly_trend': monthly_trend,
        
        # New context
        'yearly_revenue': yearly_revenue,
        'quarterly_growth': quarterly_growth,
        'current_year': current_year,
        'top_data_users': top_data_users,
        'bandwidth_stats': bandwidth_stats,
        'bandwidth_alerts': bandwidth_alerts[:5],  # Limit to 5 alerts
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)