from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, People, Relationships, Families

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name', 'password1', 'password2')
            }
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)