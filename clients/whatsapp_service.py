import os
from twilio.rest import Client
from django.conf import settings
from .models import Client
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        # Twilio credentials - you'll get these from twilio.com
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
        self.whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')  # Twilio sandbox number
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_whatsapp_message(self, to_number, message):
        """Send single WhatsApp message"""
        try:
            # Format number to WhatsApp format
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            message = self.client.messages.create(
                from_=self.whatsapp_from,
                body=message,
                to=to_number
            )
            
            logger.info(f"WhatsApp message sent to {to_number}: {message.sid}")
            return {'success': True, 'message_sid': message.sid}
            
        except Exception as e:
            logger.error(f"WhatsApp send failed to {to_number}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def send_bulk_whatsapp(self, client_ids, message_template):
        """Send bulk WhatsApp to multiple clients"""
        results = {
            'successful': [],
            'failed': []
        }
        
        clients = Client.objects.filter(id__in=client_ids)
        
        for client in clients:
            # Personalize message
            personalized_message = message_template.replace(
                '{name}', client.first_name
            ).replace(
                '{username}', client.username
            ).replace(
                '{plan}', client.service_plan.name
            )
            
            # Send message
            result = self.send_whatsapp_message(client.phone, personalized_message)
            
            if result['success']:
                results['successful'].append({
                    'client': client.full_name,
                    'phone': client.phone,
                    'message_sid': result.get('message_sid')
                })
            else:
                results['failed'].append({
                    'client': client.full_name,
                    'phone': client.phone,
                    'error': result.get('error')
                })
        
        return results
    
    def send_payment_reminder(self, client_ids):
        """Send automated payment reminders"""
        message_template = """Hello {name}! 

This is a friendly reminder that your payment for {plan} is due. 

Username: {username}

Please make payment to avoid service interruption.

Thank you!"""
        
        return self.send_bulk_whatsapp(client_ids, message_template)
    
    def send_service_update(self, client_ids, update_message):
        """Send service updates/announcements"""
        message_template = f"""Hello {{name}}!

Important Service Update:

{update_message}

Thank you for being our valued customer!"""
        
        return self.send_bulk_whatsapp(client_ids, message_template)