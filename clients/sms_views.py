from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client
from .sms_service import send_client_sms
from django.utils import timezone

def send_bulk_sms(request):
    """Send SMS to multiple clients"""
    if request.method == 'POST':
        client_ids = request.POST.getlist('clients')
        message = request.POST.get('message', '')
        
        if not client_ids or not message:
            messages.error(request, "Please select clients and enter a message")
            return redirect('sms_compose')
        
        success_count = 0
        for client_id in client_ids:
            try:
                client = Client.objects.get(id=client_id)
                if client.phone:
                    # Personalize message
                    personalized_message = message
                    personalized_message = personalized_message.replace('[Name]', client.first_name)
                    personalized_message = personalized_message.replace('[Amount]', str(client.monthly_rate))
                    personalized_message = personalized_message.replace('[Date]', str(client.next_billing_date))
                    
                    # Send SMS
                    result = send_client_sms(client.phone, personalized_message)
                    if result and result.get('status') == 'success':
                        success_count += 1
            except Client.DoesNotExist:
                continue
        
        messages.success(request, f"✅ Sent {success_count} SMS messages successfully! (Mock Mode)")
        return redirect('client_list')
    
    clients = Client.objects.filter(status='Active')
    return render(request, 'sms/compose_sms.html', {'clients': clients})

def send_payment_reminder(request, client_id):
    """Send payment reminder to single client"""
    try:
        client = Client.objects.get(id=client_id)
        message = f"Hello {client.first_name}, your internet payment of KSH {client.monthly_rate} is due on {client.next_billing_date}. Pay via M-Pesa to 0706315742. Africa Online Networks"
        
        result = send_client_sms(client.phone, message)
        messages.success(request, f"✅ Payment reminder sent to {client.phone} (Mock Mode)")
    except Client.DoesNotExist:
        messages.error(request, "❌ Client not found")
    
    return redirect('client_list')
