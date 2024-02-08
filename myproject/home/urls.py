# home/urls.py

from django.urls import path
from .views import *
from django.contrib.auth.views import (LoginView, LogoutView)

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('', HomeView.as_view(), name='home'),
    path('import-info/', import_info, name='import_info'),
    path('family/<int:family_id>', FamilyTreeView, name='family'),
    path('birth-date/', BirthDateView.as_view(), name='birth_date'),
    path('married-date/', MarriedDateView.as_view(), name='married_date'),
    path('death-date/', DeathDateView.as_view(), name='death_date'),
    path('update-info/', UpdateInfoView.as_view(), name='update_info'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # api
    path('api/find-people/', find_people, name='find_people'),
    path('api/update-people/', update_people, name='update_people'),
    path('api/find-people-in-family/', find_people_with_relationship, name='find_people_with_relationship'),
    path('api/count-people/', count_people, name='count_people'),
]
