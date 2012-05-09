from django.db import models

from jmbo.models import ModelBase


class Download(ModelBase):
  file = models.FileField(
    upload_to='downloads/',
    max_length=255
  )