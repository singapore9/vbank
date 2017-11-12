from django.utils.deprecation import MiddlewareMixin
from drf_secure_token.middleware import UpdateTokenMiddleware as _UpdateTokenMiddleware
from drf_secure_token.models import Token
from drf_secure_token.settings import settings as token_settings


class UpdateTokenMiddleware(MiddlewareMixin, _UpdateTokenMiddleware):
    # Removed token on every request.
    def process_response(self, request, response):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not isinstance(token, Token):
            if not isinstance(token, str):
                return response
            else:
                token_key = token.split()[-1]
                if Token.objects.filter(key=token_key).exists():
                    token = Token.objects.get(key=token_key)
                else:
                    return response

        if token_settings.UPDATE_TOKEN:
            new_token = Token.objects.create(user=token.user)
            response['X-Token'] = new_token.key
            token.check_token()
        return response
