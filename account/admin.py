from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'date_joined', 'is_active', 'is_staff', 'is_manager',)
    list_display_links = ('first_name', 'email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ("email",)
    readonly_fields = ('password',)


admin.site.register(Account, AccountAdmin)
