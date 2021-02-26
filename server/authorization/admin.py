from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.http import HttpResponseRedirect
# Register your models here.
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mobile',)}),
    )
    list_display = ('username', 'email', 'mobile', "first_name", 'last_name', 'is_staff')


admin.site.register(User, CustomUserAdmin)
