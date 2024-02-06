# home/urls.py

from django.urls import path
from .views import *
from django.contrib.auth.views import (LoginView, LogoutView)

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('', HomeView.as_view(), name='home'),
    
    # path('', index, name='index'),
    path('import-info/', import_info, name='import_info'),
    path('find-people/', find_people, name='find_people'),
    path('update-people/', update_people, name='update_people'),
    
    path('family/<int:family_id>', FamilyView, name='family'),
    path('birth-date/', BirthDateView.as_view(), name='birth_date'),
    path('married-date/', MarriedDateView.as_view(), name='married_date'),
    path('death-date/', DeathDateView.as_view(), name='death_date'),
]
