from django.http import HttpResponse
from django.shortcuts import render

def billing_dashboard(request):
    '''Billing dashboard'''
    return HttpResponse('''
    <html>
    <head>
        <meta charset=\"UTF-8\">
        <title>Billing Dashboard - Africa Online</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
            .button { background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class=\"header\">
            <h1>💰 Billing Dashboard</h1>
        </div>
        <div style=\"margin: 20px 0;\">
            <p>Welcome to the Billing Dashboard.</p>
            <a href=\"/\" class=\"button\">🏠 Main Dashboard</a>
            <a href=\"/admin/\" class=\"button\">⚙️ Admin Panel</a>
            <a href=\"/admin/billing/\" class=\"button\">📊 Manage Billing</a>
        </div>
    </body>
    </html>
    ''')
