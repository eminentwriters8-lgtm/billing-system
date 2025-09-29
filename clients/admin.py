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
