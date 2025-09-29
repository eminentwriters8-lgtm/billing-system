import requests
import base64
from datetime import datetime
import json
from django.conf import settings

class MpesaGateway:
    def __init__(self):
        self.consumer_key = "YOUR_CONSUMER_KEY"  # You'll get this from Safaricom
        self.consumer_secret = "YOUR_CONSUMER_SECRET"  # You'll get this from Safaricom
        self.business_shortcode = "174379"  # Lipa Na M-Pesa shortcode
        self.passkey = "YOUR_PASSKEY"  # From Safaricom
        self.callback_url = "https://yourdomain.com/mpesa-callback/"  # Your callback URL
        
    def get_access_token(self):
        """Get M-Pesa API access token"""
        try:
            url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
            auth_string = f"{self.consumer_key}:{self.consumer_secret}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {encoded_auth}"
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()["access_token"]
            return None
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """Initiate STK push to customer"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
                
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = base64.b64encode(
                f"{self.business_shortcode}{self.passkey}{timestamp}".encode()
            ).decode()
            
            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            
            payload = {
                "BusinessShortCode": self.business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": self.business_shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": self.callback_url,
                "AccountReference": account_reference,
                "TransactionDesc": transaction_desc
            }
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
            
        except Exception as e:
            print(f"Error in STK push: {e}")
            return None

# Mock M-Pesa service for development (remove in production)
class MockMpesaGateway:
    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """Mock STK push for development"""
        print(f"Mock M-Pesa: Sending STK push to {phone_number} for KSH {amount}")
        return {
            "ResponseCode": "0",
            "ResponseDescription": "Success",
            "MerchantRequestID": "mock-12345",
            "CheckoutRequestID": "mock-checkout-12345"
        }

# Use mock for development, real for production
mpesa_gateway = MockMpesaGateway()
