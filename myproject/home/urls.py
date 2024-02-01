# home/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('import-info/', import_info, name='import_info'),
    path('find-people/', find_people, name='find_people'),
    path('update-people/', update_people, name='update_people'),
]
