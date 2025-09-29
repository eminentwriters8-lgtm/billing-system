import requests
from django.conf import settings

class KenyaSMSService:
    def __init__(self):
        self.sender_id = "0706315742"
    
    def format_phone(self, phone_number):
        """Format Kenyan phone numbers"""
        phone_number = phone_number.replace(" ", "").replace("-", "")
        
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]
        elif phone_number.startswith("+254"):
            phone_number = phone_number[1:]
        elif phone_number.startswith("254"):
            pass
        else:
            phone_number = "254" + phone_number
        
        return phone_number
    
    def send_sms_mock(self, phone_number, message):
        """Mock SMS service for testing"""
        formatted_phone = self.format_phone(phone_number)
        print(f"📱 MOCK SMS from {self.sender_id} to {formatted_phone}: {message}")
        return {
            "status": "success",
            "message": "SMS sent successfully (MOCK MODE)",
            "recipient": formatted_phone,
            "cost": "KES 0.00 (Mock)"
        }

# Global SMS service
sms_service = KenyaSMSService()

def send_client_sms(phone_number, message):
    return sms_service.send_sms_mock(phone_number, message)
