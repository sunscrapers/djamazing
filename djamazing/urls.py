from django.conf.urls import url

from djamazing.views import FileView

urlpatterns = [
    url(r'^(?P<filename>[^\/]+)/', FileView.as_view())
]
