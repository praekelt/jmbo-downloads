import os.path

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site

from downloads.models import Download
from downloads.signals import download_requested

RES_DIR = os.path.join(os.path.dirname(__file__), 'res')
FILE_PATH = os.path.join(RES_DIR, 'test_file.py')


class DownloadsTestCase(TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(
            self.username, 'user@host.com', self.password
        )
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.signal_received = False
        settings.DOWNLOAD_SERVE_FROM = 'LOCAL'

    def make_download(self, file_path=None, title='some_title'):
        if file_path is None:
            # Just grab this actual file as a test file
            file_path = os.path.join(settings.PROJECT_ROOT, 'downloads',
                                     __file__)
        content_file = DjangoFile(open(FILE_PATH, 'r'), 'test_file.py')
        dl = Download.objects.create(file=content_file, title=title,
                                     image=content_file, state='published')
        # Must publish it to a site for it to become available
        dl.sites.add(Site.objects.all()[0])
        return dl

    def receive_signal(self, sender, **kwargs):
        self.signal_received = True

    def test_authentication_required(self):
        '''Downloads should be accessible without authentication by default'''
        self.client.logout()
        dl = self.make_download()
        response = self.client.get(
            reverse('download-request', kwargs={'slug': dl.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_header_is_being_set(self):
        '''Nginx header must be set for the server to serve the file'''
        dl = self.make_download()
        response = self.client.get(
            reverse('download-request', kwargs={'slug': dl.slug})
        )
        self.assertEqual(response['X-Accel-Redirect'], dl.file.url)

    def test_duplicate_filenames(self):
        """Two files with the same name are uploaded"""
        dl1 = self.make_download()
        dl2 = self.make_download()
        self.assertNotEqual(dl1.file.path, dl2.file.path)

    def test_files_are_removed(self):
        '''Check that uploaded file is deleted when object is removed'''
        dl = self.make_download()
        dl.delete()
        self.assertFalse(os.path.exists(dl.file.path))

    def test_signal_is_sent(self):
        dl = self.make_download()
        self.signal_received = False
        download_requested.connect(self.receive_signal)
        self.client.get(
            reverse('download-request', kwargs={'slug': dl.slug})
        )
        self.assertTrue(self.signal_received)

    def test_serve_using_redirect(self):
        dl = self.make_download()
        settings.DOWNLOAD_SERVE_FROM = 'REMOTE'
        r = self.client.get(reverse('download-request',
                                    kwargs={'slug': dl.slug}))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r['Location'].split('/', 4)[4], dl.file.url)
