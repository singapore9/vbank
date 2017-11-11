from __future__ import absolute_import

from django.contrib import admin
from drf_secure_token.admin import TokenAdmin
from drf_secure_token.models import Token


class CustomTokenAdmin(TokenAdmin):
    list_display = ('key', 'user', 'created', 'expire_in', 'dead_in', 'marked_for_delete', )
    list_filter = ('user', )
    search_fields = ('key', 'user__first_name',
                     'user__last_name', 'user__email', )


admin.site.unregister(Token)
admin.site.register(Token, CustomTokenAdmin)
