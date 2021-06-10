from django.contrib import admin
from django.contrib.auth.models import Group

from account.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'date_joined',
        'last_login',
        'is_admin',
        'is_superuser',
        'is_staff'
    )
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = ()


admin.site.unregister(Group)
