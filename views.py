from django.shortcuts import render
from django.http import JsonResponse
import random
from django.utils import timezone

# NETWORK MONITOR FUNCTIONS - ADD THESE TO YOUR EXISTING views.py

def network_dashboard(request):
    """Network monitoring dashboard"""
    return render(request, 'network/dashboard.html')

def network_live_dashboard(request):
    """Live network dashboard"""
    return render(request, 'network/dashboard.html')

def network_traffic_api(request):
    """API endpoint for network traffic data"""
    data = [{
        'Timestamp': timezone.now().strftime('%H:%M:%S'),
        'Download': round(random.uniform(50, 200), 1),
        'Upload': round(random.uniform(20, 80), 1),
        'TotalUsage': round(random.uniform(70, 280), 1),
        'ActiveSessions': random.randint(100, 400)
    }]
    
    return JsonResponse({
        'success': True,
        'data': data,
        'timestamp': timezone.now().isoformat()
    })

def network_alerts_api(request):
    """API endpoint for network alerts"""
    alerts = []
    if random.random() > 0.7:
        alerts.append({
            'Severity': 'LOW',
            'Message': 'High latency detected on router 2',
            'Timestamp': timezone.now().strftime('%H:%M:%S')
        })
    
    return JsonResponse({
        'success': True,
        'alerts': alerts
    })

def network_health_check(request):
    """API endpoint for network health"""
    health_data = {
        'status': 'online',
        'uptime': '99.8%',
        'current_usage': round(random.uniform(50, 200), 1),
        'active_sessions': random.randint(100, 400),
        'download_speed': round(random.uniform(80, 150), 1),
        'upload_speed': round(random.uniform(30, 70), 1),
        'latency': random.randint(8, 25),
        'health_score': random.randint(85, 100)
    }
    
    return JsonResponse({
        'success': True,
        'health': health_data
    })

def network_usage_breakdown(request):
    """API endpoint for usage breakdown"""
    usage_data = {
        'streaming': random.randint(20, 45),
        'web_browsing': random.randint(15, 30),
        'gaming': random.randint(5, 15),
        'downloads': random.randint(10, 25),
        'voip': random.randint(3, 8)
    }
    
    return JsonResponse({
        'success': True,
        'usage_breakdown': usage_data
    })

def network_peak_hours(request):
    """API endpoint for peak hours"""
    peak_data = {
        'morning': random.randint(40, 65),
        'afternoon': random.randint(50, 75),
        'evening': random.randint(70, 95),
        'night': random.randint(20, 40)
    }
    
    return JsonResponse({
        'success': True,
        'peak_hours': peak_data
    })

def combined_dashboard(request):
    """Combined billing and network dashboard"""
    return render(request, 'dashboard/combined.html')