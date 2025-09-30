from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Client, ServicePlan, Payment, IPPool

class ClientResource(resources.ModelResource):
    service_plan = fields.Field(
        column_name='service_plan',
        attribute='service_plan',
        widget=ForeignKeyWidget(ServicePlan, 'name')
    )
    ip_pool = fields.Field(
        column_name='ip_pool',
        attribute='ip_pool', 
        widget=ForeignKeyWidget(IPPool, 'name')
    )
    
    class Meta:
        model = Client
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone', 
            'address', 'service_plan', 'username', 'ipv4_address',
            'mac_address', 'latitude', 'longitude', 'physical_address',
            'monthly_rate', 'status', 'connection_status',
            'registration_date', 'installation_date', 'last_seen_online',
            'mpesa_number', 'last_payment_date', 'last_payment_amount'
        )
        export_order = fields

class ServicePlanResource(resources.ModelResource):
    class Meta:
        model = ServicePlan
        fields = ('id', 'name', 'bandwidth', 'price', 'data_cap', 'duration_hours')

class PaymentResource(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'username')
    )
    service_plan = fields.Field(
        column_name='service_plan',
        attribute='service_plan',
        widget=ForeignKeyWidget(ServicePlan, 'name')
    )
    
    class Meta:
        model = Payment
        fields = ('id', 'client', 'amount', 'mpesa_number', 'transaction_id', 
                 'payment_date', 'status', 'service_plan')

class IPPoolResource(resources.ModelResource):
    class Meta:
        model = IPPool
        fields = ('id', 'name', 'network', 'subnet_mask', 'gateway', 
                 'start_ip', 'end_ip', 'dns_servers')