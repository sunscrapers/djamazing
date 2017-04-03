import django
import sys


if django.VERSION >= (1, 10, 0):
    from django.urls import reverse  # noqa
    from django.views import View  # noqa
else:
    from django.core.urlresolvers import reverse  # noqa
    from django.views.generic.base import View  # noqa

if sys.version_info >= (3,):
    from urllib.parse import urlencode  # noqa
else:
    from urllib import urlencode  # noqa
