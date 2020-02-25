from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('turbofan/', TemplateView.as_view(template_name='turbofan.html'), name='turbofan'),
    path('turbojet/', TemplateView.as_view(template_name='turbojet.html'), name='turbojet'),
    path('plot/', include('plot.urls', namespace='plot'), name='plot'),
]