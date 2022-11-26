from django.contrib import admin

from .models import User


class UserInline(admin.TabularInline):
    model = User
    fields = ('username', 'email', 'is_staff', 'is_active', 'last_login')
    readonly_fields = ('username', 'email', 'is_staff', 'is_active', 'last_login')
    can_delete = False
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'roommates_group', 'email', 'first_name', 'last_name',
              'is_staff', 'is_active', 'last_login', 'groups')
    readonly_fields = ('last_login',)
    list_display = ('username', 'roommates_group', 'email', 'is_staff', 'is_active', 'last_login')
    list_editable = ('is_staff', 'is_active')
