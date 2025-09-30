# MOBILE APP API SYSTEM
# Copyright (c) 2025 Martin Mutinda

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Client, Invoice, Payment
from .serializers import ClientSerializer, InvoiceSerializer

class MobileAppAPI:
    @api_view(['GET'])
    def client_dashboard_mobile(request):
        """Mobile-optimized client dashboard"""
        client = request.user.client_set.first()
        
        data = {
            'client_info': {
                'name': client.name,
                'account_balance': client.get_balance(),
                'next_payment_date': client.get_next_payment_date(),
            },
            'recent_invoices': InvoiceSerializer(
                client.invoice_set.order_by('-created_at')[:5], 
                many=True
            ).data,
            'network_usage': {
                'used': client.get_data_usage(),
                'limit': client.plan.data_limit,
                'remaining': client.get_remaining_data()
            }
        }
        return Response(data)
        
    @api_view(['POST'])
    def mobile_payment(request):
        """Process mobile payment"""
        # Integrate with M-Pesa API
        amount = request.data.get('amount')
        phone = request.data.get('phone')
        
        # M-Pesa integration logic here
        payment_result = self.process_mpesa_payment(phone, amount)
        
        if payment_result['success']:
            return Response({'status': 'success', 'receipt': payment_result['receipt']})
        else:
            return Response({'status': 'failed', 'error': payment_result['error']})
            
    def process_mpesa_payment(self, phone, amount):
        """Integrate with Safaricom M-Pesa"""
        # Mock implementation - replace with actual M-Pesa API
        return {
            'success': True,
            'receipt': f'MPESA_R{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'amount': amount,
            'phone': phone
        }

mobile_api = MobileAppAPI()
