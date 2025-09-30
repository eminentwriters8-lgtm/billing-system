# Create a new clean admin.py file using PowerShell
@"
from django.contrib import admin
from .models import Client, Payment, ServicePlan

admin.site.register(Client)
admin.site.register(Payment)
admin.site.register(ServicePlan)
"@ | Out-File -FilePath "clients\admin.py" -Encoding utf8