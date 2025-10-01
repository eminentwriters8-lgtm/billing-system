# COMPLETE CLIENT MODELS WITH ALL FEATURES
# Copyright (c) 2025 Martin Mutinda

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .mikrotik_integration import mikrotik_manager

class ServicePlan(models.Model):
    PLAN_TYPES = [
        ('pppoe', 'PPPoE'),
        ('hotspot', 'Hotspot'),
        ('business', 'Business Fiber'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default='pppoe')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    speed = models.CharField(max_length=50, default='10Mbps/5Mbps')
    data_limit = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - KSH {self.price}"
        
    def get_active_clients_count(self):
        return self.client_set.filter(is_active=True).count()

class Client(models.Model):
    CLIENT_TYPES = [
        ('pppoe', 'PPPoE'),
        ('hotspot', 'Hotspot'),
        ('business', 'Business'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('inactive', 'Inactive'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    id_number = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    
    # Service Information
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPES, default='pppoe')
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.PROTECT, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    
    # Billing Information
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_payment_date = models.DateField(blank=True, null=True)
    next_payment_date = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    registration_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.username})"
    
    def save(self, *args, **kwargs):
        # Set monthly fee from service plan if not set
        if not self.monthly_fee and self.service_plan:
            self.monthly_fee = self.service_plan.price
            
        # Set next payment date if not set
        if not self.next_payment_date:
            self.next_payment_date = datetime.now().date() + timedelta(days=30)
            
        # Create MikroTik user if new client
        if not self.pk:  # New client
            try:
                if self.client_type == 'pppoe':
                    success, message = mikrotik_manager.create_pppoe_user(
                        self.username, self.password
                    )
                elif self.client_type == 'hotspot':
                    success, message = mikrotik_manager.create_hotspot_user(
                        self.username, self.password
                    )
            except Exception as e:
                print(f"Warning: Could not create MikroTik user: {e}")
            
        super().save(*args, **kwargs)
    
    def get_balance_status(self):
        """Get client balance status"""
        if self.balance >= 0:
            return 'paid'
        elif self.balance < 0 and self.balance >= -self.monthly_fee:
            return 'pending'
        else:
            return 'overdue'
    
    def get_days_overdue(self):
        """Calculate days overdue"""
        if self.next_payment_date and self.next_payment_date < datetime.now().date():
            return (datetime.now().date() - self.next_payment_date).days
        return 0
    
    def get_connection_status(self):
        """Check if client is currently connected via MikroTik"""
        try:
            active_connections = mikrotik_manager.get_active_connections()
            if self.client_type == 'pppoe':
                for connection in active_connections.get('pppoe', []):
                    if connection.get('name') == self.username:
                        return True
            elif self.client_type == 'hotspot':
                for connection in active_connections.get('hotspot', []):
                    if connection.get('user') == self.username:
                        return True
            return False
        except:
            return False

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client.name}"
    
    def generate_invoice_number(self):
        """Generate unique invoice number"""
        if not self.invoice_number:
            date_str = datetime.now().strftime('%Y%m%d')
            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=date_str
            ).order_by('-invoice_number').first()
            
            if last_invoice:
                last_num = int(last_invoice.invoice_number[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
                
            self.invoice_number = f"{date_str}-{new_num:04d}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.generate_invoice_number()
        super().save(*args, **kwargs)

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit Card'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='mpesa')
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment of KSH {self.amount} by {self.client.name}"
    
    def save(self, *args, **kwargs):
        # Update client balance
        if self.client:
            self.client.balance -= self.amount
            self.client.last_payment_date = datetime.now().date()
            self.client.next_payment_date = datetime.now().date() + timedelta(days=30)
            self.client.save()
            
        # Update invoice status if applicable
        if self.invoice:
            self.invoice.status = 'paid'
            self.invoice.paid_at = datetime.now()
            self.invoice.save()
            
        super().save(*args, **kwargs)

class NetworkUsage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    download_bytes = models.BigIntegerField(default=0)
    upload_bytes = models.BigIntegerField(default=0)
    usage_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['client', 'usage_date']
        ordering = ['-usage_date']
    
    def __str__(self):
        return f"Usage for {self.client.name} on {self.usage_date}"
    
    def get_total_bytes(self):
        return self.download_bytes + self.upload_bytes
    
    def get_formatted_usage(self):
        """Return formatted usage in appropriate units"""
        total_bytes = self.get_total_bytes()
        if total_bytes >= 1024**3:  # GB
            return f"{(total_bytes / 1024**3):.2f} GB"
        elif total_bytes >= 1024**2:  # MB
            return f"{(total_bytes / 1024**2):.2f} MB"
        else:  # KB
            return f"{(total_bytes / 1024):.2f} KB"

class SystemSettings(models.Model):
    """System configuration settings"""
    SETTING_TYPES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('boolean', 'Boolean'),
        ('decimal', 'Decimal'),
    ]
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    value_type = models.CharField(max_length=20, choices=SETTING_TYPES, default='string')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'
        ordering = ['key']
    
    def __str__(self):
        return f"{self.key} = {self.value}"
    
    def get_typed_value(self):
        """Return the value in the correct data type"""
        if self.value_type == 'integer':
            return int(self.value) if self.value else 0
        elif self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes')
        elif self.value_type == 'decimal':
            from decimal import Decimal
            return Decimal(self.value) if self.value else Decimal('0.00')
        else:
            return self.value

class SystemResetLog(models.Model):
    """Log of system reset operations"""
    RESET_TYPES = [
        ('clients', 'Clients Only'),
        ('financial', 'Financial Data'),
        ('all', 'Complete Reset'),
        ('custom', 'Custom Reset'),
    ]
    
    reset_type = models.CharField(max_length=20, choices=RESET_TYPES)
    description = models.TextField()
    reset_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    clients_deleted = models.IntegerField(default=0)
    invoices_deleted = models.IntegerField(default=0)
    payments_deleted = models.IntegerField(default=0)
    reset_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-reset_date']
    
    def __str__(self):
        return f"Reset {self.reset_type} on {self.reset_date.strftime('%Y-%m-%d %H:%M')}"
