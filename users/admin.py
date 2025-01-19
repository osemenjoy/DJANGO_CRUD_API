from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomuserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}), # this adds the roles field to the admin page,if it is not none then it will add a title
    )


admin.site.register(CustomUser, CustomuserAdmin)