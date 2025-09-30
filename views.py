from django.shortcuts import render, redirect
from django.contrib import messages
from .whatsapp_service import WhatsAppService
import json

def whatsapp_bulk_send(request):
    if request.method == 'POST':
        client_ids = request.POST.getlist('clients')
        message = request.POST.get('message', '')
        
        if not client_ids or not message:
            messages.error(request, "Please select clients and enter a message")
            return redirect('whatsapp_compose')
        
        whatsapp_service = WhatsAppService()
        results = whatsapp_service.send_bulk_whatsapp(client_ids, message)
        
        # Store results in session to display
        request.session['whatsapp_results'] = results
        
        messages.success(request, f"Sent {len(results['successful'])} messages successfully!")
        if results['failed']:
            messages.warning(request, f"Failed to send {len(results['failed'])} messages")
        
        return redirect('whatsapp_results')
    
    # GET request - show compose form
    clients = Client.objects.filter(status='Active')
    return render(request, 'whatsapp/compose.html', {'clients': clients})

def whatsapp_results(request):
    results = request.session.get('whatsapp_results', {})
    return render(request, 'whatsapp/results.html', {'results': results})

def whatsapp_payment_reminders(request):
    if request.method == 'POST':
        client_ids = request.POST.getlist('clients')
        
        whatsapp_service = WhatsAppService()
        results = whatsapp_service.send_payment_reminder(client_ids)
        
        request.session['whatsapp_results'] = results
        messages.success(request, f"Sent payment reminders to {len(results['successful'])} clients")
        return redirect('whatsapp_results')
    
    # Show clients with upcoming payments
    from datetime import datetime, timedelta
    upcoming_clients = Client.objects.filter(
        next_billing_date__lte=datetime.now().date() + timedelta(days=3),
        status='Active'
    )
    return render(request, 'whatsapp/reminders.html', {'clients': upcoming_clients})