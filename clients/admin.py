from django.contrib import admin
from .models import Client, ServicePlan

@admin.register(ServicePlan)
class ServicePlanAdmin(admin.ModelAdmin):
    list_display = ["name", "bandwidth", "price", "data_cap"]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["full_name", "username", "service_type", "status", "monthly_rate", "next_billing_date"]
    list_filter = ["service_type", "status"]
    search_fields = ["first_name", "last_name", "username"]
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'ipv4_address', 'installation_date', 'last_seen_online', 'physical_address']
from .models import IPPool

@admin.register(IPPool)
class IPPoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'network', 'subnet_mask', 'gateway', 'start_ip', 'end_ip']
from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin, ExportActionMixin
from .models import Client, ServicePlan, Payment, IPPool, UserProfile
from .resources import ClientResource, ServicePlanResource, PaymentResource, IPPoolResource

@admin.register(Client)
class ClientAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ClientResource
    list_display = [
        'first_name', 'last_name', 'username', 'ipv4_address', 
        'service_plan', 'status', 'connection_status', 'last_seen_online'
    ]
    list_filter = ['status', 'connection_status', 'service_plan']
    search_fields = ['first_name', 'last_name', 'username', 'ipv4_address']
    actions = ['export_selected_clients']

@admin.register(ServicePlan)
class ServicePlanAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ServicePlanResource
    list_display = ['name', 'bandwidth', 'price', 'data_cap']

@admin.register(Payment)
class PaymentAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PaymentResource
    list_display = ['client', 'amount', 'mpesa_number', 'payment_date', 'status']
    list_filter = ['status', 'payment_date']

@admin.register(IPPool)
class IPPoolAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = IPPoolResource
    list_display = ['name', 'network', 'subnet_mask', 'gateway', 'start_ip', 'end_ip']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_picture']
