from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from clients.models.bank_accounts import BankAccount
from clients.models.bank_cards import BankCard
from clients.models.members import Member


def make_confirmed_by_bank(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_confirmed_by_bank.short_description = "Confirm by bank manager"


def make_nonconfirmed_by_bank(modeladmin, request, queryset):
    queryset.filter(role=Member.CLIENT).update(is_active=False)
make_nonconfirmed_by_bank.short_description = "Remove confirmation by bank manager"


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
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_confirmed')
    list_filter = ('role', 'is_active')
    search_fields = ('first_name', 'last_name', 'middle_name', 'email', )
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-id',)
    actions = UserAdmin.actions + [make_confirmed_by_bank, make_nonconfirmed_by_bank]

    def get_readonly_fields(self, request, obj=None):
        g = Group.objects.filter(name='bank_admin')
        if request.user and g.exists() and g.first().user_set.filter(email=request.user.email):
            return ['username', 'password', 'last_name', 'first_name', 'middle_name', 'email', 'birthday',
                    'residence_address', 'role', 'is_confirmed', 'is_staff', 'is_superuser', 'date_joined',
                    'last_login', ]
        else:
            return ['last_login', 'date_joined']


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('holder', 'number', 'balance', 'currency')
    list_filter = ('holder', 'currency')
    raw_id_fields = ('holder', )

    def get_readonly_fields(self, request, obj=None):
        return ['number', 'holder', 'currency'] if obj else ['number', ]


@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    list_display = ('holder', 'number')
    raw_id_fields = ('bank_account', )

    def get_readonly_fields(self, request, obj=None):
        return ['holder', 'number', 'bank_account'] if obj else ['number', 'holder']
