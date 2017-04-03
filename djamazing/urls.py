from django.conf.urls import url

from djamazing.views import FileView

app_name = 'djamazing'

urlpatterns = [
    url(r'', FileView.as_view(), name='protected_file'),
]
