import os.path
import uuid

from mimetypes import guess_type

from django.db.models import F
from django.core.files import File
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _

import Image, ImageFont, ImageDraw

from jmbo.view_modifiers import DefaultViewModifier
from jmbo.generic.views import GenericObjectDetail, GenericObjectList

from foundry.settings import MEDIA_ROOT

from downloads.models import Download, DOWNLOAD_ROOT


# where temporary downloadable files are kept
TEMP_ROOT = 'tmp/'


def download_request(request, file_name, re_file_name=None):
  file_path = os.path.join(DOWNLOAD_ROOT,file_name)
  # check if download is not temporary
  try:
    download = Download.objects.get(file=file_path)    
    # increment view count
    download.view_count += 1
    download.save()
    f = download.file
  except Download.DoesNotExist:
    pass
  
  mime = guess_type(file_name)
  response = HttpResponse(content_type=mime[0])
  
  # check if it has encoding
  if mime[1]:
    response['Content-Encoding'] = mime[1]
  if re_file_name:
    response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(re_file_name)
  else:
    response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(os.path.basename(file_name))
  response['Cache-Control'] = 'no-cache'
  response['X-Accel-Redirect'] = smart_str(os.path.join('/media/', file_path))
  
  return response


class ObjectList(GenericObjectList):
    
    def get_extra_context(self, *args, **kwargs):
        return {'title': _('Downloads')}
        
    def get_queryset(self, *args, **kwargs):
        return Download.permitted.all()
    
    def get_paginate_by(self, *args, **kwargs):
        return 20

object_list = ObjectList()


class ImageModView(object):
    # absolute path to modified image files
    IMAGE_MOD_ROOT = os.path.join(MEDIA_ROOT,os.path.join(DOWNLOAD_ROOT, TEMP_ROOT))
    
    def make_file_name(self, id_number):
        if id_number:
            return str(uuid.UUID(int=id_number)) + '.jpg'
        else: 
            return str(uuid.uuid4()) + '.jpg'
        
    # override this for different modifications and return image
    def create_modified_image(self, *args, **kwargs):
        pass
        
    def download_modified_image(self, request, id_number, re_file_name, *args, **kwargs):
        file_name = self.make_file_name(id_number)
        file_path = os.path.join(self.IMAGE_MOD_ROOT, file_name)
        # check if file exists
        try:
            f = open(file_path)
            f.close()
        # if not, create the file
        except IOError:
            image = self.create_modified_image(*args, **kwargs)
            image.save(file_path)
            
        return download_request(request, os.path.join(TEMP_ROOT, file_name), re_file_name)
        
    def __call__(self, request, id_number, re_file_name, *args, **kwargs):
        return self.download_modified_image(request, id_number, re_file_name, *args, **kwargs)

        
class TextOverlayImageModView(ImageModView):
    
    # box = (x, y, width, height); base_image = Django FileField instance
    def __init__(self, font, text_size, color, box, base_image):
        #self.base_image = Image.open(base_image.url)
        self.base_image = base_image
        self.box = box
        self.font = ImageFont.truetype(font, text_size)
        self.color = color
        
    def draw_text(self, drawable, pos, text):
        drawable.text(pos, text, font=self.font, fill=self.color)
            
    def create_modified_image(self, text):
        image = self.base_image.copy()
        draw =  ImageDraw.Draw(image)
        # draw text with line breaking
        height = 0
        line = ''
        for word in text.split(' '):
            size = self.font.getsize(line + word)
            if size[0] > self.box[2]:
                self.draw_text(draw, (self.box[0], self.box[1] + height), line[0:-1])
                line = word + ' '
                height += size[1]
            else:
                line += word + ' '
        self.draw_text(draw, (self.box[0], self.box[1] + height), line[0:-1])
        del draw
        
        return image
        
    def __call__(self, request, id_number, re_file_name, text):
        return super(TextOverlayImageModView, self).__call__(request, id_number, re_file_name, text)

text_overlay = TextOverlayImageModView(
    "/usr/share/fonts/truetype/msttcorefonts/impact.ttf", 
    40, 
    (255, 255, 255), 
    (0, 0, 200, 200), 
    Image.open(os.path.join(os.path.join(MEDIA_ROOT, DOWNLOAD_ROOT), "1_800x600.jpg"))
)
