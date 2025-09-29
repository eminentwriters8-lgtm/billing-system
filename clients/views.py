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
