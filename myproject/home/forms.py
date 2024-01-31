from django import forms
from .models import People

class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = '__all__'  # Bao gồm tất cả các trường của model
