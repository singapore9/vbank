from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets
from django.contrib.admin.sites import site
from django import forms
from mailing.shortcuts import render_send_email

from clients.models.bank_accounts import BankAccount
from clients.models.bank_cards import BankCard
from clients.models.members import Member


def make_confirmed_by_bank(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_confirmed_by_bank.short_description = "Confirm by bank manager"


def make_locked_by_bank(modeladmin, request, queryset):
    queryset.filter(role=Member.CLIENT).update(is_locked=True)
make_locked_by_bank.short_description = "Lock by bank manager"


class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):

    def save(self, commit=True):
        password = self.cleaned_data["password1"]
        user = super(CustomAdminPasswordChangeForm, self).save(commit)
        context = {
            'password': password
        }
        template_name = 'email/reset_pass/transfer_notification'
        render_send_email([user.email], template_name, context, use_base_template=False)
        return user


@admin.register(Member)
class MemberAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('last_name', 'first_name', 'middle_name', 'email', 'birthday',
                                         'residence_address')}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_confirmed', 'is_locked', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_confirmed', 'is_locked')
    list_filter = ('role', 'is_active')
    search_fields = ('first_name', 'last_name', 'middle_name', 'email', )
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-id',)
    change_password_form = CustomAdminPasswordChangeForm
    actions = UserAdmin.actions + [make_confirmed_by_bank, make_locked_by_bank]

    def get_readonly_fields(self, request, obj=None):
        g = Group.objects.filter(name='bank_admin')
        if request.user and g.exists() and g.first().user_set.filter(email=request.user.email):
            return ['username', 'password', 'last_name', 'first_name', 'middle_name', 'email', 'birthday',
                    'residence_address', 'role', 'is_confirmed', 'is_staff', 'is_superuser', 'date_joined',
                    'last_login', ]
        else:
            return ['last_login', 'date_joined']


class HolderRawIdWidget(widgets.ForeignKeyRawIdWidget):
    def url_parameters(self):
        res = super().url_parameters()
        res['role__exact'] = Member.CLIENT
        return res


class BankAccountAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get('holder'):
            self.fields['holder'].queryset = Member.objects.filter(role=Member.CLIENT)
            self.fields['holder'].widget = HolderRawIdWidget(rel=BankAccount._meta.get_field('holder').rel, admin_site=site)

    class Meta:
        fields = '__all__'
        model = BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    form = BankAccountAdminForm
    list_display = ('holder', 'number', 'balance', 'currency')
    search_fields = ('holder__email', 'holder__first_name', 'holder__last_name', 'holder__middle_name', 'number')
    list_filter = ('holder', 'currency')
    raw_id_fields = ('holder', )

    def get_readonly_fields(self, request, obj=None):
        return ['number', 'holder', 'currency'] if obj else ['number', ]


@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    list_display = ('holder', 'number')
    search_fields = ('holder__email', 'holder__first_name', 'holder__last_name', 'holder__middle_name', 'number', 'bank_account__number')
    list_filter = ('holder', 'bank_account')
    raw_id_fields = ('bank_account', )

    def get_readonly_fields(self, request, obj=None):
        return ['holder', 'number', 'bank_account'] if obj else ['number', 'holder']
