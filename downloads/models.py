from django.db import models

from jmbo.models import ModelBase


class Download(ModelBase):
  downloadable_file = models.FileField(
    upload_to='downloads/',
    max_length=255
  )