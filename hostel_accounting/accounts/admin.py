from django.contrib import admin

from .models import User, RoommatesGroup


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'roommates_group', 'email', 'first_name', 'last_name',
              'is_staff', 'is_active', 'last_login')
    readonly_fields = ('last_login',)
    list_display = ('username', 'roommates_group', 'email', 'is_staff', 'is_active', 'last_login')
    list_editable = ('is_staff', 'is_active')


class UserInline(admin.TabularInline):
    model = User
    fields = ('username', 'roommates_group', 'email', 'is_staff', 'is_active', 'last_login')
    readonly_fields = ('username', 'email', 'is_staff', 'is_active', 'last_login')
    can_delete = False
    extra = 0


@admin.register(RoommatesGroup)
class RoommatesGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'created_at')
    readonly_fields = ('created_at',)
    list_display = ('name', 'created_at')
    inlines = (UserInline,)
