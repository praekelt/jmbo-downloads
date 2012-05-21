import os.path

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site

from downloads.models import Download


class DownloadsTestCase(TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(
            self.username, 'user@host.com', self.password
        )
        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def make_download(self, file_path=None, title='some_title'):
        if file_path is None:
            # Just grab this actual file as a test file
            file_path = os.path.join(settings.PROJECT_ROOT, 'downloads',
                            __file__)
        dl = Download.objects.create(file=DjangoFile(open(
                                                file_path), 'test_file.py'),
                                                title=title,
                                                state='published')
        # Must publish it to a site for it to become available
        dl.sites.add(Site.objects.all()[0])
        return dl

    def test_authentication_required(self):
        self.client.logout()
        dl = self.make_download()
        file_name = dl.file.name.split('/', 1)[1]
        response = self.client.get(
            reverse('download_request', kwargs={'file_name': file_name})
        )
        self.assertEqual(response.status_code, 302)
        
    def test_header_is_being_set(self):
        dl = self.make_download()
        slug = dl.slug
        response = self.client.get(reverse('download-request', args=(slug,)))
        self.assertEqual(response['X-Accel-Redirect'],
            '%sdownloads/%s' % (settings.MEDIA_URL,
            os.path.basename(dl.file.name)))

    def test_duplicate_filenames(self):
        """Two files with the same name are uploaded"""
        dl1 = self.make_download()
        dl2 = self.make_download()
        self.assertNotEqual(dl1.file.path, dl2.file.path)

