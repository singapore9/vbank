from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from members.models.bank_accounts import BankAccount
from members.models.bank_cards import BankCard
from members.models.members import Member


@admin.register(Member)
class MemberAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('last_name', 'first_name', 'middle_name', 'email', 'birthday',
                                         'residence_address')}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_confirmed', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active')
    search_fields = ('first_name', 'last_name', 'middle_name', 'email', )
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-id',)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('holder', 'number', 'balance', 'currency')
    list_filter = ('holder', 'currency')

    def get_readonly_fields(self, request, obj=None):
        return ['number', 'holder'] if obj else []


@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    list_display = ('holder', 'number')

    def get_readonly_fields(self, request, obj=None):
        return ['holder', 'number'] if obj else []
