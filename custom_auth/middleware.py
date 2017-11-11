from django.utils.deprecation import MiddlewareMixin
from drf_secure_token.middleware import UpdateTokenMiddleware as _UpdateTokenMiddleware


class UpdateTokenMiddleware(MiddlewareMixin, _UpdateTokenMiddleware):
    pass
