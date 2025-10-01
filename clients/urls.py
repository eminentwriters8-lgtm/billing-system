from django.urls import path
from . import views
from .views import create_admin

urlpatterns = [
    path('create-admin/', create_admin, name='create_admin'),
    # Main Dashboard & Navigation
    path('', views.main_dashboard, name='main_dashboard'),
    path('dashboard/', views.combined_dashboard, name='combined_dashboard'),
    
    # Client Management
    path('clients/', views.client_list, name='client_list'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('clients/management/', views.client_management, name='client_management'),
    path('clients/location/<int:client_id>/', views.client_location_pin, name='client_location_pin'),
    path('clients/location/save/<int:client_id>/', views.save_client_location, name='save_client_location'),
    
    # Billing & Financial
    path('billing/', views.billing_dashboard, name='billing_dashboard'),
    path('billing/management/', views.billing_management, name='billing_management'),
    path('billing/reports/', views.reports_dashboard, name='reports_dashboard'),
    
    # Network Management
    path('network/', views.network_dashboard, name='network_dashboard'),
    path('network/live/', views.network_live_dashboard, name='network_live_dashboard'),
    path('network/sync/', views.sync_mikrotik_users, name='sync_mikrotik_users'),
    
    # Network API Endpoints
    path('network/api/traffic/', views.network_traffic_api, name='network_traffic_api'),
    path('network/api/alerts/', views.network_alerts_api, name='network_alerts_api'),
    path('network/api/health/', views.network_health_api, name='network_health_api'),
    path('network/api/usage/', views.network_usage_api, name='network_usage_api'),
    path('network/api/peak-hours/', views.network_peak_hours_api, name='network_peak_hours_api'),
    path('network/health-check/', views.network_health_check, name='network_health_check'),
    path('network/usage-breakdown/', views.network_usage_breakdown, name='network_usage_breakdown'),
    path('network/peak-hours/', views.network_peak_hours, name='network_peak_hours'),
    
    # Messaging
    path('messaging/', views.whatsapp_compose, name='whatsapp_compose'),
    path('messaging/results/', views.whatsapp_results, name='whatsapp_results'),
    path('messaging/reminders/', views.whatsapp_reminders, name='whatsapp_reminders'),
    
    # System Management
    path('system/', views.system_management, name='system_management'),
    path('system/reset/', views.reset_system_data, name='reset_system_data'),
    path('system/initialize/', views.initialize_system, name='initialize_system'),
    path('system/stats/', views.get_system_stats, name='get_system_stats'),
    
    # Auto-login (for development)
    path('auto-login/', views.auto_login, name='auto_login'),
    
    # Data APIs
    path('api/dashboard/', views.get_real_dashboard_data, name='get_real_dashboard_data'),
]

