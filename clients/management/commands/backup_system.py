import os
import json
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
from clients.models import Client, Invoice, Payment, SystemSettings
from datetime import datetime

class Command(BaseCommand):
    help = 'Backup system data and send via email'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            action='store_true',
            help='Send backup via email'
        )
        parser.add_argument(
            '--path',
            type=str,
            help='Custom backup path'
        )

    def handle(self, *args, **options):
        send_email = options['email']
        custom_path = options['path']
        
        self.stdout.write('?? Creating system backup...')
        
        # Create backup data
        backup_data = {
            'timestamp': timezone.now().isoformat(),
            'clients': self.backup_clients(),
            'invoices': self.backup_invoices(),
            'payments': self.backup_payments(),
            'system_info': self.backup_system_info()
        }
        
        # Save to file
        backup_path = self.save_backup(backup_data, custom_path)
        
        if send_email:
            self.email_backup(backup_path, backup_data)
            
        self.stdout.write(self.style.SUCCESS(f'? Backup completed: {backup_path}'))
        
    def backup_clients(self):
        \"\"\"Backup client data\"\"\"
        clients = Client.objects.all()
        return [
            {
                'id': client.id,
                'name': client.name,
                'email': client.email,
                'phone': client.phone,
                'service_plan': str(client.service_plan) if client.service_plan else None,
                'balance': float(client.balance),
                'is_active': client.is_active,
                'created_at': client.created_at.isoformat()
            }
            for client in clients
        ]
        
    def backup_invoices(self):
        \"\"\"Backup invoice data\"\"\"
        invoices = Invoice.objects.all()
        return [
            {
                'invoice_number': invoice.invoice_number,
                'client': invoice.client.name,
                'amount': float(invoice.amount),
                'status': invoice.status,
                'due_date': invoice.due_date.isoformat(),
                'created_at': invoice.created_at.isoformat()
            }
            for invoice in invoices
        ]
        
    def backup_payments(self):
        \"\"\"Backup payment data\"\"\"
        payments = Payment.objects.all()
        return [
            {
                'client': payment.client.name,
                'amount': float(payment.amount),
                'payment_method': payment.payment_method,
                'payment_date': payment.payment_date.isoformat(),
                'transaction_id': payment.transaction_id
            }
            for payment in payments
        ]
        
    def backup_system_info(self):
        \"\"\"Backup system settings and info\"\"\"
        return {
            'total_clients': Client.objects.count(),
            'total_invoices': Invoice.objects.count(),
            'total_payments': Payment.objects.count(),
            'total_revenue': sum(float(p.amount) for p in Payment.objects.all()),
            'backup_time': timezone.now().isoformat()
        }
        
    def save_backup(self, backup_data, custom_path=None):
        \"\"\"Save backup to file\"\"\"
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if custom_path:
            backup_dir = custom_path
        else:
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            
        os.makedirs(backup_dir, exist_ok=True)
        
        filename = f'backup_{timestamp}.json'
        filepath = os.path.join(backup_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
        return filepath
        
    def email_backup(self, backup_path, backup_data):
        \"\"\"Send backup via email\"\"\"
        try:
            backup_email = SystemSettings.objects.filter(key='backup_email').first()
            if not backup_email:
                self.stdout.write(self.style.WARNING('?? No backup email configured'))
                return
                
            email = EmailMessage(
                subject=f'Africa Online Backup - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                body=self.create_email_body(backup_data),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[backup_email.value]
            )
            
            # Attach backup file
            with open(backup_path, 'rb') as f:
                email.attach(f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', f.read(), 'application/json')
                
            email.send()
            self.stdout.write(self.style.SUCCESS('? Backup email sent'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'? Email failed: {e}'))
            
    def create_email_body(self, backup_data):
        \"\"\"Create email body with backup summary\"\"\"
        return f\"\"\"
Africa Online Billing System - Data Backup

Backup Summary:
• Clients: {len(backup_data['clients'])}
• Invoices: {len(backup_data['invoices'])}
• Payments: {len(backup_data['payments'])}
• Total Revenue: KSH {backup_data['system_info']['total_revenue']:,.2f}

Backup Time: {backup_data['timestamp']}

This is an automated backup from your Africa Online Billing System.
\"\"\"
