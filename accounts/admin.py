from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'last_login', 'date_joined', 'is_active', 'is_staff')
    list_display_links = ('email',)
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ('is_staff',)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
