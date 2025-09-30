# Update your clients/dashboard_views.py file
python -c "
content = '''from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from decimal import Decimal
from ..clients.models import Client, Payment, ServicePlan

def admin_dashboard(request):
    # Basic statistics
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(status='active').count()
    suspended_clients = Client.objects.filter(status='suspended').count()
    
    # Monthly revenue (from Payment model)
    current_month = timezone.now().month
    monthly_revenue = Payment.objects.filter(
        payment_date__month=current_month,
        status='Completed'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Service plan statistics - use ServicePlan price instead of monthly_rate
    service_stats = ServicePlan.objects.annotate(
        client_count=Count('client'),
        total_revenue=Sum('price')
    ).values('service_type', 'client_count', 'total_revenue')
    
    # Alert panels
    today = timezone.now().date()
    overdue_clients = Client.objects.filter(
        next_billing_date__lt=today,
        status='active'
    )
    expiring_soon = Client.objects.filter(
        next_billing_date__range=[today, today + timedelta(days=7)],
        status='active'
    )
    
    # Recent payments
    recent_payments = Payment.objects.select_related('client').order_by('-payment_date')[:5]
    
    # Monthly trend
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_trend = Payment.objects.filter(
        payment_date__gte=six_months_ago,
        status='Completed'
    ).extra({
        'month': \"strftime('%%Y-%%m', payment_date)\"
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
    
    # NEW: Placeholder for Data Usage & Bandwidth Monitoring
    # (You'll need to implement this based on your actual data usage tracking)
    bandwidth_stats = {
        'total': 1000,  # Example: 1000 GB total capacity
        'used': 650,    # Example: 650 GB used
        'usage_percentage': 65,
        'peak_morning': 45,
        'peak_afternoon': 65,
        'peak_evening': 85,
    }
    
    top_data_users = []  # Placeholder - implement based on your DataUsage model
    bandwidth_alerts = []  # Placeholder
    
    context = {
        'total_clients': total_clients,
        'active_clients': active_clients,
        'suspended_clients': suspended_clients,
        'monthly_revenue': monthly_revenue,
        'service_stats': service_stats,
        'overdue_clients': overdue_clients,
        'expiring_soon': expiring_soon,
        'recent_payments': recent_payments,
        'monthly_trend': monthly_trend,
        'yearly_revenue': yearly_revenue,
        'quarterly_growth': quarterly_growth,
        'current_year': current_year,
        'top_data_users': top_data_users,
        'bandwidth_stats': bandwidth_stats,
        'bandwidth_alerts': bandwidth_alerts,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)
'''

with open('clients/dashboard_views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ Fixed dashboard_views.py')
"