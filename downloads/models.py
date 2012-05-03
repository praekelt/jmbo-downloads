from django.db import models
from jmbo import ModelBase

class Download(ModelBase):
  downloadable_file = models.FileField(
    unique=True
  )