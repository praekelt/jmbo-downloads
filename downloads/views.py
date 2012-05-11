import os.path

from mimetypes import guess_type

from django.db.models import F
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _

from jmbo.view_modifiers import DefaultViewModifier
from jmbo.generic.views import GenericObjectDetail, GenericObjectList

from downloads.models import Download


def download_request(request, file_name):
  download = Download.objects.get(file='downloads/'+file_name)
  
  # increment view count
  download.view_count += 1
  download.save()
  
  f = download.file
  
  mime = guess_type(f.name)
  response = HttpResponse(content_type=mime[0])
  
  # check if it has encoding
  if mime[1]:
    respones['Content-Encoding'] = mime[1]
  response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(file_name)
  response['Cache-Control'] = 'no-cache'
  response['X-Accel-Redirect'] = smart_str(f.url)
  
  return response
  

class ObjectList(GenericObjectList):
    
    def get_extra_context(self, *args, **kwargs):
        return {'title': _('Downloads')}
        
    def get_queryset(self, *args, **kwargs):
        return Download.permitted.all()
    
    def get_paginate_by(self, *args, **kwargs):
        return 20

object_list = ObjectList()