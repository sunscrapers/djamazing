from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.views import View
from django.core.files.storage import get_storage_class

from djamazing.storage import check_signature


class FileView(View):
    def __init__(self, storage=None):
        if storage is None:
            self.storage = get_storage_class()()
        else:
            self.storage = storage()

    def get(self, request, filename):
        username = request.user.get_username()
        signature = request.GET['signature']
        if not check_signature(signature, filename, username):
            return HttpResponseForbidden()
        return HttpResponseRedirect(
            redirect_to=self.storage.cloud_front_url(filename)
        )
