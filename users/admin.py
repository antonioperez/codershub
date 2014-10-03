from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import HubUser

# Register your models here.

class HubUserInline(admin.StackedInline):
    model = HubUser
    can_delete = False

class HubUserAdmin(UserAdmin):
    inlines = (HubUserInline, )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, HubUserAdmin)

