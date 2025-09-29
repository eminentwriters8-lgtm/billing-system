from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# Change admin site titles with support info
admin.site.site_header = "Africa Online Networks Administration - Support: 0706315742"
admin.site.site_title = "Africa Online Networks"
admin.site.index_title = "Welcome to Africa Online Networks Admin - Support: 0706315742"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls')),
    path('', RedirectView.as_view(url='/clients/dashboard/')),
]
