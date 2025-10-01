from django import forms
from .models import Client, ServicePlan

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name', 'email', 'phone', 'id_number', 'address', 
            'client_type', 'service_plan', 'username', 'password',
            'monthly_fee', 'latitude', 'longitude'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Physical Address', 'rows': 3}),
            'client_type': forms.Select(attrs={'class': 'form-control'}),
            'service_plan': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username for services'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'monthly_fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Fee', 'step': '0.01'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude', 'step': '0.000001'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_plan'].queryset = ServicePlan.objects.filter(is_active=True)
        self.fields['client_type'].choices = [
            ('', 'Select Client Type'),
            ('Residential', 'Residential'),
            ('Business', 'Business'),
            ('Corporate', 'Corporate'),
        ]
