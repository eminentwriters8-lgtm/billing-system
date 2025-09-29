from django.shortcuts import render, redirect
from .models import Client, ServicePlan
from .forms import ClientForm

def client_list(request):
    clients = Client.objects.all().order_by("-registration_date")
    return render(request, "clients/client_list.html", {"clients": clients})

def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("client_list")
    else:
        form = ClientForm()
    
    # Get all service plans for the dropdown
    service_plans = ServicePlan.objects.all()
    return render(request, "clients/client_form.html", {
        "form": form,
        "service_plans": service_plans
    })
import json
from django.http import JsonResponse

def save_client_location(request, client_id):
    if request.method == 'POST':
        try:
            client = Client.objects.get(id=client_id)
            data = json.loads(request.body)
            client.latitude = data.get('latitude')
            client.longitude = data.get('longitude')
            client.save()
            return JsonResponse({'status': 'success'})
        except Client.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Client not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
def client_location_pin(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/location_pin.html', {'client': client})
from django.shortcuts import get_object_or_404, render

def client_location_pin(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/location_pin.html', {'client': client})
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404