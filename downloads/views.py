import os.path
import uuid

from mimetypes import guess_type

from django.db.models import F
from django.core.files import File
from django.conf.settings import MEDIA_ROOT
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _

from PIL import Image

from jmbo.view_modifiers import DefaultViewModifier
from jmbo.generic.views import GenericObjectDetail, GenericObjectList

from downloads.models import Download


# root of all downloadable files
DOWNLOAD_ROOT = 'downloads/'
# where temporary downloadable files are kept
TEMP_ROOT = 'tmp/'


def download_request(request, file_name):
  download = Download.objects.get(file=os.path.join(DOWNLOAD_ROOT,file_name))
  
  # increment view count
  download.view_count += 1
  download.save()
  
  f = download.file
  
  mime = guess_type(f.name)
  response = HttpResponse(content_type=mime[0])
  
  # check if it has encoding
  if mime[1]:
    response['Content-Encoding'] = mime[1]
  response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(file_name)
  response['Cache-Control'] = 'no-cache'
  response['X-Accel-Redirect'] = smart_str(f.url)
  
  return response
  

class ImageModView(object):
    # absolute path to modified image files
    IMAGE_MOD_ROOT = os.path.join(MEDIA_ROOT,os.path.join(DOWNLOAD_ROOT, TEMP_ROOT))
    
    def make_file_name(self, id_number):
        if id_number:
            return str(uuid.UUID(int=id_number)) + '.jpg'
        else: 
            return uuid.uuid4() + '.jpg'
        
    # override this for different modifications and return image
    def create_modified_image(self, *args, **kwargs):
        pass
        
    def download_modified_image(self, request, id_number, *args, **kwargs):
        file_name = make_file_name(id_number)
        file_path = os.path.join(self.IMAGE_MOD_ROOT, file_name)
        # check if file exists
        try:
            f = open(file_path)
            f.close()
        # if not, create the file
        except IOError:
            image = create_modified_image(args, kwargs)
            image.save(file_path)
            
        return download_request(request, os.path.join(TEMP_ROOT, file_name))
        
    def __call__(self, request, id_number=None, *args, **kwargs):
        return download_modified_image(request, id_number, *args, **kwargs)

        
class TextOverlayImageModView(ImageModView):
    
    # text_box = (x, y, width, height); base_image = Django FileField instance
    def __init__(self, text_box, base_image):
        self.base_image = Image.open(base_image.url)
        self.text_box = text_box
            
    def create_modified_image(self, text):
        image =  self.base_image.copy()
        return image
    

class ObjectList(GenericObjectList):
    
    def get_extra_context(self, *args, **kwargs):
        return {'title': _('Downloads')}
        
    def get_queryset(self, *args, **kwargs):
        return Download.permitted.all()
    
    def get_paginate_by(self, *args, **kwargs):
        return 20

object_list = ObjectList()