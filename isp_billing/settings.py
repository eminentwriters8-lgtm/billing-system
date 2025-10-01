'''
# Billing System - Africa Online Networks
# Copyright (c) 2025 Martin Mutinda. All Rights Reserved.
# 
# Proprietary Software - Unauthorized copying, modification, distribution,
# or use of this software via any medium is strictly prohibited.
# 
# This software is the confidential and proprietary information of
# Martin Mutinda ("Confidential Information"). You shall not disclose
# such Confidential Information and shall use it only in accordance
# with the terms of the license agreement.
# 
# For licensing inquiries:
# ?? Email: martinmutinda@africaonlinenetworks.co.ke
# ?? Phone: +254 706 315 742
# 
# Developed with ?? by Martin Mutinda
'''

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

DEBUG = True

# Allow all hosts for development
ALLOWED_HOSTS = ['billing-system-1-j6uu.onrender.com', '.onrender.com', 'localhost', '127.0.0.1']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clients',
    'billing',
    'crispy_forms',
    'crispy_bootstrap5',
    'import_export',  # ADD THIS LINE
]



# MikroTik Router Configuration
MIKROTIK_HOST = '192.168.88.1'  # Replace with your MikroTik IP
MIKROTIK_USERNAME = 'admin'     # Replace with your username
MIKROTIK_PASSWORD = ''          # Replace with your password
MIKROTIK_PORT = 8728

# System Configuration
SYSTEM_NAME = 'Africa Online Networks'
SYSTEM_VERSION = 'Enterprise v2.0'
DEVELOPER = 'Martin Mutinda'
SUPPORT_EMAIL = 'martinmutinda@africaonlinenetworks.co.ke'

# FORCE CLIENTS ADMIN REGISTRATION
import sys
if 'runserver' in sys.argv:
    try:
        from django.apps import apps
        from django.contrib import admin
        clients_app = apps.get_app_config('clients')
        for model in clients_app.get_models():
            if not admin.site.is_registered(model):
                admin.site.register(model)
        print('Forced clients admin registration')
    except Exception as e:
        print(f'Force registration failed: {e}')







