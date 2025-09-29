from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "Africa Online Networks Administration"
    site_title = "Africa Online Networks"
    index_title = "Welcome to Africa Online Networks Admin"

custom_admin_site = CustomAdminSite(name='custom_admin')
