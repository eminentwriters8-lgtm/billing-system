from django.db import models
from django.utils import timezone
from datetime import timedelta

class ServicePlan(models.Model):
    name = models.CharField(max_length=100)
    bandwidth = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    data_cap = models.CharField(max_length=50, blank=True, null=True)
    duration_hours = models.IntegerField(default=720)  # 30 days default
    
    def __str__(self):
        return f"{self.name} - KSH {self.price}"

class Client(models.Model):
    SERVICE_TYPES = [
        ("PPPoE", "PPPoE"),
        ("Hotspot", "Hotspot"),
    ]
    
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Suspended", "Suspended"),
        ("Inactive", "Inactive"),
    ]
    
    CONNECTION_STATUS = [
        ("Connected", "Connected"),
        ("Disconnected", "Disconnected"),
        ("Expired", "Expired"),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Service Information
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPES)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    
    # Billing Information
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.PROTECT)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    connection_status = models.CharField(max_length=12, choices=CONNECTION_STATUS, default="Disconnected")
    
    # Dates
    registration_date = models.DateField(auto_now_add=True)
    next_billing_date = models.DateField()
    payment_expiry = models.DateTimeField(blank=True, null=True)
    
    # MikroTik Integration
    mikrotik_profile = models.CharField(max_length=50, default="default")
    is_synced = models.BooleanField(default=False)
    
    # M-Pesa Payment
    mpesa_number = models.CharField(max_length=20, default="0706315742")
    last_payment_date = models.DateTimeField(blank=True, null=True)
    last_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_payment_active(self):
        if self.payment_expiry:
            return self.payment_expiry > timezone.now()
        return False
    
    def update_payment_status(self):
        if self.payment_expiry and self.payment_expiry < timezone.now():
            self.connection_status = "Expired"
            self.save()

class Payment(models.Model):
    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_number = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default="Pending")
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Payment {self.amount} - {self.client.username}"
