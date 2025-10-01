from django.core.management.base import BaseCommand
from django.contrib import admin
from django.apps import apps

class Command(BaseCommand):
    help = 'Verify admin registration'
    
    def handle(self, *args, **options):
        print('=== VERIFYING ADMIN REGISTRATION ===')
        
        try:
            clients_app = apps.get_app_config('clients')
            print(f'Clients app: {clients_app.name}')
            
            for model in clients_app.get_models():
                registered = admin.site.is_registered(model)
                status = '✓' if registered else '✗'
                print(f'{status} {model.__name__}: {registered}')
                
            print(f'Total models registered: {len(admin.site._registry)}')
            
        except Exception as e:
            print(f'Error: {e}')
