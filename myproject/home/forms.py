from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import People, CustomUser

class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = '__all__'  # Bao gồm tất cả các trường của model


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)