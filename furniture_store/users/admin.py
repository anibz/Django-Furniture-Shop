from django.contrib import admin

# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """მომხმარებლების Admin პანელი"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'address']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    fieldsets = UserAdmin.fieldsets + (
        ('დამატებითი ინფორმაცია', {
            'fields': ('phone', 'address', 'birth_date')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('დამატებითი ინფორმაცია', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'birth_date')
        }),
    )