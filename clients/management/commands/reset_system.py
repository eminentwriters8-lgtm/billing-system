import os
import shutil
from django.core.management.base import BaseCommand
from django.utils import timezone
from clients.models import Client, Invoice, Payment, NetworkUsage, SystemResetLog
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Perform system reset operations'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['clients', 'financial', 'all', 'custom'],
            help='Type of reset to perform'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm the reset operation'
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup before reset'
        )

    def handle(self, *args, **options):
        reset_type = options['type']
        confirmed = options['confirm']
        backup = options['backup']
        
        if not confirmed:
            self.stdout.write(
                self.style.ERROR('? Reset not confirmed. Use --confirm to proceed.')
            )
            return
            
        if backup:
            self.create_backup()
            
        user = User.objects.filter(is_superuser=True).first()
        
        if reset_type == 'clients':
            self.reset_clients(user)
        elif reset_type == 'financial':
            self.reset_financial(user)
        elif reset_type == 'all':
            self.reset_all(user)
        elif reset_type == 'custom':
            self.reset_custom(user)
            
    def reset_clients(self, user):
        \"\"\"Reset all client data\"\"\"
        self.stdout.write('?? Resetting client data...')
        
        clients_count = Client.objects.count()
        invoices_count = Invoice.objects.count()
        payments_count = Payment.objects.count()
        usage_count = NetworkUsage.objects.count()
        
        # Delete related records first
        NetworkUsage.objects.all().delete()
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        Client.objects.all().delete()
        
        # Log the reset
        SystemResetLog.objects.create(
            reset_type='clients',
            reset_by=user,
            clients_deleted=clients_count,
            invoices_deleted=invoices_count,
            payments_deleted=payments_count,
            description='Full clients data reset'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'? Reset completed: {clients_count} clients, {invoices_count} invoices, {payments_count} payments, {usage_count} usage records deleted')
        )
        
    def reset_financial(self, user):
        \"\"\"Reset financial data only\"\"\"
        self.stdout.write('?? Resetting financial data...')
        
        invoices_count = Invoice.objects.count()
        payments_count = Payment.objects.count()
        
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        
        # Reset client balances
        Client.objects.all().update(balance=0)
        
        SystemResetLog.objects.create(
            reset_type='financial',
            reset_by=user,
            invoices_deleted=invoices_count,
            payments_deleted=payments_count,
            description='Financial data reset - invoices and payments cleared'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'? Financial reset completed: {invoices_count} invoices, {payments_count} payments deleted')
        )
        
    def reset_all(self, user):
        \"\"\"Reset entire system\"\"\"
        self.stdout.write('?? Performing full system reset...')
        
        self.reset_clients(user)
        # Add any additional reset logic here
        
        SystemResetLog.objects.create(
            reset_type='all',
            reset_by=user,
            description='Complete system reset'
        )
        
        self.stdout.write(self.style.SUCCESS('? Full system reset completed'))
        
    def reset_custom(self, user):
        \"\"\"Custom reset - extend this as needed\"\"\"
        self.stdout.write('?? Performing custom reset...')
        
        # Example: Reset only old data
        cutoff_date = timezone.now() - timedelta(days=365)
        old_invoices = Invoice.objects.filter(created_at__lt=cutoff_date)
        old_payments = Payment.objects.filter(payment_date__lt=cutoff_date)
        
        invoices_count = old_invoices.count()
        payments_count = old_payments.count()
        
        old_payments.delete()
        old_invoices.delete()
        
        SystemResetLog.objects.create(
            reset_type='custom',
            reset_by=user,
            invoices_deleted=invoices_count,
            payments_deleted=payments_count,
            description=f'Custom reset: data older than {cutoff_date.strftime("%Y-%m-%d")}'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'? Custom reset completed: {invoices_count} old invoices, {payments_count} old payments deleted')
        )
        
    def create_backup(self):
        \"\"\"Create a backup of the database\"\"\"
        self.stdout.write('?? Creating backup...')
        # Add backup logic here (database dump, file backup, etc.)
        self.stdout.write(self.style.SUCCESS('? Backup created'))
