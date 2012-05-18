import os.path

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
from django.core.urlresolvers import reverse
from django.conf import settings

from downloads.models import Download


class DownloadsTestCase(TestCase):

    def setUp(self):
        self.username = 'user'
        self.password = 'password'
        self.user = User.objects.create_user(self.username, self.password,
                                                'user@host.com')
        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def make_download(self, file_path=None, file_name='test_file'):
        if file_path is None:
            # Just grab this actual file as a test file
            file_path = os.path.join(settings.PROJECT_ROOT, 'downloads',
                            __file__)
        return Download.objects.create(file=DjangoFile(open(
                                                file_path), 'test_file.py'))

    def test_header_is_being_set(self):
        download = self.make_download()
        response = self.client.get(reverse('download_request', kwargs={
            'file_name': download.file.name,
        }))
        self.assertEqual(response['X-Accel-Redirect'], 'bla')
