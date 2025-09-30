from django.urls import path
from . import views

urlpatterns = [
    # Existing WhatsApp URLs
    path('whatsapp/compose/', views.whatsapp_bulk_send, name='whatsapp_compose'),
    path('whatsapp/results/', views.whatsapp_results, name='whatsapp_results'),
    path('whatsapp/reminders/', views.whatsapp_payment_reminders, name='whatsapp_reminders'),
    
    # New Network Monitor URLs
    path('network/dashboard/', views.network_dashboard, name='network_dashboard'),
    path('network/live/', views.network_live_dashboard, name='network_live_dashboard'),
    path('network/api/traffic/', views.network_traffic_api, name='network_traffic_api'),
    path('network/api/alerts/', views.network_alerts_api, name='network_alerts_api'),
    path('network/api/health/', views.network_health_check, name='network_health_check'),
    path('network/api/usage/', views.network_usage_breakdown, name='network_usage_api'),
    path('network/api/peak-hours/', views.network_peak_hours, name='network_peak_hours'),
    path('dashboard/combined/', views.combined_dashboard, name='combined_dashboard'),
]
