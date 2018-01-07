import django
import sys


if django.VERSION >= (1, 10, 0):
    from django.urls import reverse  # noqa
    from django.views import View  # noqa
    from django.utils.deprecation import MiddlewareMixin
    from threadlocals.middleware import ThreadLocalMiddleware as OldThreadLocalMiddleware

    class ThreadLocalMiddleware(OldThreadLocalMiddleware, MiddlewareMixin):
        pass
else:
    from django.core.urlresolvers import reverse  # noqa
    from django.views.generic.base import View  # noqa
    from threadlocals.middleware import ThreadLocalMiddleware

if sys.version_info >= (3,):
    from urllib.parse import urlencode  # noqa
else:
    from urllib import urlencode  # noqa
