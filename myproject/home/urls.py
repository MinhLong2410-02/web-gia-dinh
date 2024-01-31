# home/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('import-info/', import_info, name='import-info'),
    path('get-people-with-relationships/', get_people_with_relationships, name='get-people-with-relationships')
]
