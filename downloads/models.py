import os.path

from django.db import models
from django.conf import settings

from jmbo.models import ModelBase

from colors.fields import ColorField


# root of all downloadable files
DOWNLOAD_ROOT = 'downloads/'
# path to base image files required for modifications
IMAGE_MOD_ROOT = os.path.join(DOWNLOAD_ROOT, 'mods/')


class Download(ModelBase):
    file = models.FileField(
        upload_to=DOWNLOAD_ROOT,
        max_length=255
    )
  
    class Meta:
        ordering = ['primary_category', 'title']


class ImageMod(ModelBase):
    download_file_name = models.CharField(max_length=255)
    unique_per_user = models.BooleanField(default=False)
    
    # override this in subclasses
    def get_view_args(self):
        pass
    
    def get_absolute_url(self):
        return '/downloads/image-mod/' + self.slug
        

class TextOverlayImageMod(ImageMod):
    base_image = models.ImageField(upload_to=IMAGE_MOD_ROOT)
    text = models.TextField()
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    colour = ColorField()
    
    def get_view_args(self):
        return [self.text]