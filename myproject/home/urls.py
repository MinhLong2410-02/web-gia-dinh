# home/urls.py

from django.urls import path
from .views import index, import_info

urlpatterns = [
    path('', index, name='index'),
    path('import-info/', import_info, name='import-info'),
]
