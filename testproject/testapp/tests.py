from django.test import TestCase, Client
from django.contrib.auth.models import User
from djet.assertions import StatusCodeAssertionsMixin
from threadlocals.threadlocals import set_current_user

from djamazing.storage import DjamazingStorage

class TestSignedUrls(TestCase, StatusCodeAssertionsMixin):

    def setUp(self):
        self.client = Client()
        self.logged = User.objects.create(username='logged')
        self.other = User.objects.create(username='other')
        for user in [self.logged, self.other]:
            user.set_password('pass')
            user.save()
        self.storage = DjamazingStorage()

    def tearDown(self):
        for user in [self.logged, self.other]:
            user.delete()

    def test_correct(self):
        """Test if correctly signed URL gets redirected"""
        set_current_user(self.logged)
        url = self.storage.url('file.txt')
        login = self.client.login(username='logged', password='pass')
        self.assertTrue(login)
        resp = self.client.get(url)
        self.assert_status_equal(resp, 302)

    def test_incorrect(self):
        """Test if URL signed for other user gets rejected"""
        set_current_user(self.other)
        url = self.storage.url('file.txt')
        login = self.client.login(username='logged', password='pass')
        self.assertTrue(login)
        resp = self.client.get(url)
        self.assert_status_equal(resp, 403)
