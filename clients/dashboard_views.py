from django.shortcuts import render
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Client, Payment, ServicePlan
import calendar

def admin_dashboard(request):
    # Current year and previous year
    current_year = timezone.now().year
    current_month = timezone.now().month
    previous_year = current_year - 1
    
    # ===== REAL DATA CALCULATIONS =====
    
    # Monthly revenue (resets each month) - CURRENT MONTH ONLY
    monthly_revenue_current = Payment.objects.filter(
        payment_date__year=current_year,
        payment_date__month=current_month,
        status='Completed'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Yearly revenue data
    yearly_revenue = {
        'total': 0,
        'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0
    }
    
    # Current year quarterly revenue
    for quarter in range(1, 5):
        start_month = (quarter - 1) * 3 + 1
        end_month = quarter * 3
        
        quarter_payments = Payment.objects.filter(
            payment_date__year=current_year,
            payment_date__month__gte=start_month,
            payment_date__month__lte=end_month,
            status='Completed'
        )
        revenue = quarter_payments.aggregate(total=Sum('amount'))['total'] or 0
        yearly_revenue[f'q{quarter}'] = float(revenue)
    
    # Total yearly revenue
    yearly_revenue['total'] = sum([yearly_revenue['q1'], yearly_revenue['q2'], yearly_revenue['q3'], yearly_revenue['q4']])
    
    # Monthly revenue trend for line graph (last 6 months)
    monthly_trend = []
    for i in range(5, -1, -1):  # Last 6 months including current
        month_date = timezone.now() - timedelta(days=30*i)
        month_year = month_date.year
        month_num = month_date.month
        
        month_payments = Payment.objects.filter(
            payment_date__year=month_year,
            payment_date__month=month_num,
            status='Completed'
        )
        revenue = month_payments.aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_trend.append({
            'month': month_date.strftime('%b'),
            'revenue': float(revenue),
            'full_month': month_date.strftime('%B %Y')
        })
    
    # Calculate quarterly growth
    quarterly_growth = []
    for quarter in range(1, 5):
        current_q_revenue = yearly_revenue[f'q{quarter}']
        previous_q_revenue = Payment.objects.filter(
            payment_date__year=previous_year,
            payment_date__month__gte=(quarter - 1) * 3 + 1,
            payment_date__month__lte=quarter * 3,
            status='Completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if previous_q_revenue > 0:
            growth = ((current_q_revenue - previous_q_revenue) / previous_q_revenue) * 100
        else:
            growth = 100 if current_q_revenue > 0 else 0
            
        quarterly_growth.append({
            'quarter': f'Q{quarter}',
            'revenue': current_q_revenue,
            'growth': round(growth, 1)
        })
    
    # Client statistics
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(status='Active').count()
    suspended_clients = Client.objects.filter(status='Suspended').count()
    
    # Total revenue (all time)
    total_revenue = Payment.objects.filter(status='Completed').aggregate(total=Sum('amount'))['total'] or 0
    
    # Service plan distribution with revenue
    service_stats = []
    service_plans = ServicePlan.objects.all()
    
    for plan in service_plans:
        plan_clients = Client.objects.filter(service_plan=plan, status='Active')
        client_count = plan_clients.count()
        
        # Calculate monthly revenue for this service plan
        plan_revenue = Payment.objects.filter(
            client__service_plan=plan,
            payment_date__year=current_year,
            payment_date__month=current_month,
            status='Completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        service_stats.append({
            'service_type': plan.name,
            'count': client_count,
            'revenue': float(plan_revenue)
        })
    
    # ===== REAL DATA FOR SIDEBAR SECTIONS =====
    
    # Recent payments (last 5 completed payments)
    recent_payments = Payment.objects.filter(status='Completed').select_related('client').order_by('-payment_date')[:5]
    
    # Top data users (you'll need to add data usage tracking to your Client model)
    # For now, using active clients as placeholder
    top_data_users = []
    active_clients_list = Client.objects.filter(status='Active')[:5]
    for client in active_clients_list:
        top_data_users.append({
            'client_name': client.full_name or client.username,
            'service_type': client.service_plan.name if client.service_plan else 'No Plan',
            'data_used': 0,  # Replace with actual data usage field
            'data_limit': 0,  # Replace with actual data limit field
            'usage_percentage': 0
        })
    
    # Bandwidth alerts (based on service usage - customize as needed)
    bandwidth_alerts = []
    high_usage_clients = Client.objects.filter(status='Active')[:3]  # Example: first 3 active clients
    for client in high_usage_clients:
        bandwidth_alerts.append({
            'client_name': client.full_name or client.username,
            'service_type': client.service_plan.name if client.service_plan else 'No Plan',
            'usage_percentage': 85,  # Replace with actual usage calculation
            'alert_type': 'high_usage'
        })
    
    # Expiring soon (clients with upcoming billing dates)
    next_week = timezone.now() + timedelta(days=7)
    expiring_soon = Client.objects.filter(
        status='Active',
        next_billing_date__lte=next_week,
        next_billing_date__gte=timezone.now()
    )[:5]
    
    # Overdue clients
    overdue_clients = Client.objects.filter(
        status='Active',
        next_billing_date__lt=timezone.now()
    )[:5]
    
    # Bandwidth stats (replace with your actual bandwidth tracking)
    # You'll need to implement bandwidth monitoring separately
    bandwidth_stats = {
        'usage_percentage': 65,
        'used': 650,
        'total': 1000,
        'peak_morning': 45,
        'peak_afternoon': 65,
        'peak_evening': 85
    }
    
    context = {
        'total_clients': total_clients,
        'active_clients': active_clients,
        'suspended_clients': suspended_clients,
        'total_revenue': total_revenue,
        'monthly_revenue': float(monthly_revenue_current),
        'monthly_revenue_current': float(monthly_revenue_current),
        'monthly_trend': monthly_trend,
        'current_year': current_year,
        'previous_year': previous_year,
        'yearly_revenue': yearly_revenue,
        'quarterly_growth': quarterly_growth,
        'service_stats': service_stats,
        'bandwidth_stats': bandwidth_stats,
        'top_data_users': top_data_users,
        'bandwidth_alerts': bandwidth_alerts,
        'recent_payments': recent_payments,
        'expiring_soon': expiring_soon,
        'overdue_clients': overdue_clients,
        'months': [calendar.month_abbr[i] for i in range(1, 13)],
        'quarters': ['Q1', 'Q2', 'Q3', 'Q4'],
    }
    
    return render(request, 'clients/dashboard_new.html', context)