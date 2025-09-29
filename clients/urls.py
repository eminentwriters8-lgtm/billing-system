# Auto-login feature added for easy access
from django.urls import path
from django.views.generic import TemplateView
from . import views
from . import dashboard_views
from . import hotspot_views
from . import sms_views
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect

def auto_login(request):
    try:
        user = User.objects.get(username='mutinda')
        login(request, user)
        return redirect('/clients/dashboard/')
    except User.DoesNotExist:
        # If user doesn't exist, create one and log in
        user = User.objects.create_user('mutinda', 'eminentwriters8@gmail.com', '123admin')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        login(request, user)
        return redirect('/clients/dashboard/')

urlpatterns = [
    path("", views.client_list, name="client_list"),
    path("new/", views.client_create, name="client_create"),
    # Dashboard
    path("dashboard/", dashboard_views.admin_dashboard, name="admin_dashboard"),
    # About page
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    # SMS URLs
    path("sms/compose/", sms_views.send_bulk_sms, name="sms_compose"),
    path("sms/reminder/<int:client_id>/", sms_views.send_payment_reminder, name="send_reminder"),
    # Hotspot URLs
    path("hotspot/login/", hotspot_views.hotspot_login, name="hotspot_login"),
    path("hotspot/process-payment/", hotspot_views.process_hotspot_payment, name="process_hotspot_payment"),
    path("hotspot/logout/", hotspot_views.hotspot_logout, name="hotspot_logout"),
    # Auto-login URL - Add this line
    path("auto-login/", auto_login, name="auto_login"),
]