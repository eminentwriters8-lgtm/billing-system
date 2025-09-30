# Create a minimal resources.py file to fix the import
@"
# Temporary minimal resources file
from import_export import resources
from .models import Client, Payment

class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        fields = ('id', 'user__username', 'status')

class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment
        fields = ('id', 'client__user__username', 'amount', 'status')
"@ | Out-File -FilePath "clients\resources.py" -Encoding utf8