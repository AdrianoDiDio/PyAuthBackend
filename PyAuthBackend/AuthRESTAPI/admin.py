from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from PyAuthBackend.AuthRESTAPI.models import User

admin.site.register(User,UserAdmin)
