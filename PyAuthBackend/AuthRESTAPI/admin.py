from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from PyAuthBackend.AuthRESTAPI.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'biometricToken',
                    'biometricChallenge',
                ),
            },
        ),
    )
admin.site.register(User,CustomUserAdmin)
