# CUSTOM ADMIN SITE - AFRICA ONLINE NETWORKS
# Copyright (c) 2025 Martin Mutinda

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.urls import reverse

class AfricaOnlineNetworksAdminSite(AdminSite):
    site_header = "Africa Online Networks - Administration"
    site_title = "Africa Online Networks"
    index_title = "Welcome to Africa Online Networks Management"
    
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request, app_label)
        
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
            
        return app_list

    def index(self, request, extra_context=None):
        """
        Override the main admin index page to add custom context
        """
        if extra_context is None:
            extra_context = {}
            
        extra_context.update({
            'system_name': 'Africa Online Networks',
            'version': 'Enterprise v2.0',
            'developer': 'Martin Mutinda',
            'support_contact': 'martinmutinda@africaonlinenetworks.co.ke'
        })
        
        return super().index(request, extra_context)

# Create custom admin site instance
admin_site = AfricaOnlineNetworksAdminSite(name='africa_online_networks_admin')

# Register default admin models
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
