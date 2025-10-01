from django.contrib import admin
from .models import Client, ServicePlan, Invoice, Payment, NetworkUsage, SystemSettings, SystemResetLog

# Remove custom header/title to use Django defaults
# admin.site.site_header = 'Django Administration'
# admin.site.site_title = 'Django site admin'
# admin.site.index_title = 'Site administration'

# Register models with basic admin classes
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'service_plan', 'is_active']
    list_filter = ['is_active', 'service_plan']
    search_fields = ['name', 'email', 'phone']

@admin.register(ServicePlan)
class ServicePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'is_active']
    list_filter = ['is_active', 'plan_type']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'client', 'amount', 'status', 'due_date']
    list_filter = ['status', 'due_date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['client', 'amount', 'payment_method', 'payment_date']
    list_filter = ['payment_method', 'payment_date']

@admin.register(NetworkUsage)
class NetworkUsageAdmin(admin.ModelAdmin):
    list_display = ['client', 'usage_date', 'download_bytes', 'upload_bytes']
    list_filter = ['usage_date']

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'is_active']
    list_filter = ['is_active']

@admin.register(SystemResetLog)
class SystemResetLogAdmin(admin.ModelAdmin):
    list_display = ['reset_type', 'reset_by', 'reset_date']
    list_filter = ['reset_type', 'reset_date']
