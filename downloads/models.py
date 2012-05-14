from django.db import models

from jmbo.models import ModelBase

from downloads.views import DOWNLOAD_ROOT

class Download(ModelBase):
  file = models.FileField(
    upload_to=DOWNLOAD_ROOT,
    max_length=255
  )
  
  class Meta:
      ordering = ['primary_category', 'title']