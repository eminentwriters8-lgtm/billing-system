'''
# Billing System - Africa Online Networks
# Copyright (c) 2025 Martin Mutinda. All Rights Reserved.
# 
# Proprietary Software - Unauthorized copying, modification, distribution,
# or use of this software via any medium is strictly prohibited.
# 
# This software is the confidential and proprietary information of
# Martin Mutinda ("Confidential Information"). You shall not disclose
# such Confidential Information and shall use it only in accordance
# with the terms of the license agreement.
# 
# For licensing inquiries:
# 📧 Email: martinmutinda@africaonlinenetworks.co.ke
# 📞 Phone: +254 706 315 742
# 
# Developed with ❤️ by Martin Mutinda
'''

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
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('inactive', 'Inactive'),
    ]
    
    CONNECTION_STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('unknown', 'Unknown'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    connection_status = models.CharField(max_length=20, choices=CONNECTION_STATUS_CHOICES, default='unknown')
    ipv4_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    next_billing_date = models.DateField(null=True, blank=True)
    last_seen_online = models.DateTimeField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    physical_address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]
    
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f'Payment {self.id}'

class DataUsage(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    data_used = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usage_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.client} - {self.data_used}GB'

