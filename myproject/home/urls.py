# home/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('import-info/', import_info, name='import-info'),
    path('find_people/', find_people, name='find_people')
]
