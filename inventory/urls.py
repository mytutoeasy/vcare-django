from django.urls import path
from django.views.generic import TemplateView

app_name = 'inventory'

urlpatterns = [
    path('', TemplateView.as_view(template_name='inventory/list.html'), name='list'),
]
