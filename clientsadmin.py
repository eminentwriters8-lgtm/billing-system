from django.contrib import admin
from .models import Client, Payment, ServicePlan

admin.site.register(Client)
admin.site.register(Payment)
admin.site.register(ServicePlan)