from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ServicePlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bandwidth = models.CharField(max_length=50)
    service_type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='active')
    connection_status = models.CharField(max_length=20, default='unknown')
    ipv4_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    next_billing_date = models.DateField(null=True, blank=True)
    last_seen_online = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='Pending')
    
    def __str__(self):
        return f"Payment {self.id}"