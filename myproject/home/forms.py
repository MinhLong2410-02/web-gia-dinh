from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
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

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Gmail',
        widget=forms.TextInput(attrs={
            'class': 'input',
            'type': 'text',
            'placeholder': 'Nhập gmail',
            'autofocus': True,
            'required': 'required'
        })
    )
    
    password = forms.CharField(label='Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'input password',
            'name': 'pass',
            'placeholder': 'Mật khẩu',
            'required': 'required'  
        }),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = False
        self.fields['password'].label = False
