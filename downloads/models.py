from django.db import models

from jmbo.models import ModelBase


# root of all downloadable files
DOWNLOAD_ROOT = 'downloads/'


class Download(ModelBase):
  file = models.FileField(
    upload_to=DOWNLOAD_ROOT,
    max_length=255
  )
  
  class Meta:
      ordering = ['primary_category', 'title']