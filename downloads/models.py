import os.path
import uuid

from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from jmbo.models import ModelBase
from jmbo.managers import PermittedManager

from downloads.fields import ColourField


# root of all downloadable files
DOWNLOAD_ROOT = 'downloads/'
# path to media required for image modifications
MOD_MEDIA_ROOT = os.path.join(DOWNLOAD_ROOT, 'mods/')
# where temporary downloadable files are kept
TEMP_ROOT = os.path.join(DOWNLOAD_ROOT, 'tmp/')


# manager that excludes invisible downloads by default
class DownloadManager(PermittedManager):

    def get_query_set(self, include_invisible=False):
        qs = super(DownloadManager, self).get_query_set()
        if not include_invisible:
            qs = qs.exclude(visible=False)
        return qs


class Download(ModelBase):
    file = models.FileField(
        upload_to=DOWNLOAD_ROOT,
        max_length=255,
        null=True,
        blank=True
    )
    file_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    visible = models.BooleanField(default=True)
    permitted = DownloadManager()

    class Meta:
        ordering = ['primary_category', 'title']

    def get_absolute_url(self):
        return reverse('download-request', args=[self.slug])

    # return 2-tuple containing the file and response file name
    def get_file(self, request):
        if self.file_name:
            return (self.file, self.file_name)
        else:
            return (self.file, os.path.basename(self.file.name))

    def delete(self):
        if os.path.exists(self.file.path):
            os.remove(self.file.path)
        super(Download, self).delete()


# abstract base class for temporary downloads
class TemporaryDownloadAbstract(Download):
    unique_per_user = models.BooleanField(default=False) #editable=False

    class Meta:
        abstract = True

    def make_file_name(self, request, extension=''):
        if self.unique_per_user:
            id = str(uuid.UUID(int=request.user.id))
        else:
            id = return str(uuid.uuid4())
        return "%s_%s.%s" % (self.slug, id, extension)

    # override this in subclasses and save resulting image in tmp
    def create_modified_image(self, file_path, request):
        pass # ad not implemented exception

    def get_file(self, request):
        file_name = self.make_file_name(request)
        file_path = os.path.join(os.path.join(settings.MEDIA_ROOT,
            TEMP_ROOT), file_name)
        # check if file exists
        try:
            f = open(file_path)
            f.close()
        # if not, create the file
        except IOError:
            self.create_modified_image(file_path, request)
        # not saved to db since the files are temporary
        self.file.name = os.path.join(TEMP_ROOT, file_name)

        return super(TemporaryDownloadAbstract, self).get_file(request)


class TextOverlayTemporaryDownload(TemporaryDownloadAbstract):
    background_image = models.ImageField(upload_to=MOD_MEDIA_ROOT)
    text = models.TextField()
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    font = models.FilePathField(
        path='/usr/share/fonts/truetype/',
        recursive=True
    )
    font_size = models.PositiveIntegerField()
    colour = ColourField()

    def make_file_name(self, request):
        return super(TextOverlayTemporaryDownload, self).make_file_name(request, 'jpg')
        
    def save(self, *args, **kwargs):
        super(TextOverlayTemporaryDownload, self).save(*args, **kwargs)
        self._image = Image.open(os.path.join(settings.MEDIA_ROOT,
            self.background_image.name))
        self._box = (self.x, self.y, self.width, self.height)
        self._font = ImageFont.truetype(self.font, self.font_size)
        self._line_height = int(self.font_size * 0.85)
        self._colour = str(self.colour)

    def draw_text(self, drawable, pos, text):
        drawable.text(pos, text, font=self._font, fill=self._colour)

    def create_modified_image(self, file_path, request):
        image = self._image.copy()
        draw = ImageDraw.Draw(image)
        # draw text with line breaking
        height = 0
        line = ''
        for word in self.text.split(' '):
            size = draw.textsize(line + word, font=self._font)
            if size[0] > self._box[2]:
                self.draw_text(draw,
                    (self._box[0], self._box[1] + height), line[0:-1])
                line = word + ' '
                height += self._line_height
            else:
                line += word + ' '
        self.draw_text(draw, (self._box[0], self._box[1] + height), line[0:-1])
        del draw
        image.save(file_path)
