from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from rest_framework.authtoken.models import Token

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
	fieldsets = DjangoUserAdmin.fieldsets + (
		("Additional", {"fields": ("bio", "profile_picture", "followers")} ),
	)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
	list_display = ("key", "user", "created")
