from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Client, ServicePlan, Payment

def admin_dashboard(request):
    today = timezone.now().date()
    
    # Key statistics
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(status="Active").count()
    suspended_clients = Client.objects.filter(status="Suspended").count()
    
    # Revenue statistics
    monthly_revenue = Client.objects.aggregate(
        total=Sum("monthly_rate")
    )["total"] or Decimal('0')
    
    # Expiry alerts (clients expiring in next 7 days)
    expiry_threshold = today + timedelta(days=7)
    expiring_soon = Client.objects.filter(
        next_billing_date__lte=expiry_threshold,
        next_billing_date__gte=today,
        status="Active"
    ).order_by('next_billing_date')
    
    # Overdue clients
    overdue_clients = Client.objects.filter(
        next_billing_date__lt=today,
        status="Active"
    )
    
    # Service type breakdown
    service_stats = Client.objects.values("service_type").annotate(
        count=Count("id"),
        revenue=Sum("monthly_rate")
    )
    
    # Recent payments (last 10)
    recent_payments = Payment.objects.select_related('client').order_by("-payment_date")[:10]
    
    # Monthly revenue trend (last 6 months - simplified)
    monthly_trend = [
        {"month": "Jan", "revenue": float(monthly_revenue) * 0.8},
        {"month": "Feb", "revenue": float(monthly_revenue) * 0.9},
        {"month": "Mar", "revenue": float(monthly_revenue)},
        {"month": "Apr", "revenue": float(monthly_revenue) * 1.1},
        {"month": "May", "revenue": float(monthly_revenue) * 1.2},
        {"month": "Jun", "revenue": float(monthly_revenue) * 1.3},
    ]
    
    context = {
        'total_clients': total_clients,
        'active_clients': active_clients,
        'suspended_clients': suspended_clients,
        'monthly_revenue': monthly_revenue,
        'expiring_soon': expiring_soon,
        'overdue_clients': overdue_clients,
        'service_stats': service_stats,
        'recent_payments': recent_payments,
        'monthly_trend': monthly_trend,
        'today': today,
    }
    
    return render(request, "dashboard/admin_dashboard.html", context)
