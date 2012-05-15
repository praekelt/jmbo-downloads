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

from django.conf import settings

from downloads.models import Download, DOWNLOAD_ROOT, \
        ImageMod


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
    IMAGE_MOD_ROOT = os.path.join(settings.MEDIA_ROOT,os.path.join(DOWNLOAD_ROOT, TEMP_ROOT))
    
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
    
    # box = (x, y, width, height); base_image = Django ImageField instance
    def __init__(self, font, text_size, color, box, base_image):
        self.base_image = Image.open(os.path.join(settings.MEDIA_ROOT, base_image.name))
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
            size = draw.textsize(line + word, font=self.font)
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

        
def image_mod(request, slug):
    mod = ImageMod.permitted.get(slug=slug).as_leaf_class()
    view = TextOverlayImageModView(
            "/usr/share/fonts/truetype/msttcorefonts/impact.ttf", 
            64, 
            '#' + str(mod.colour), 
            (mod.x, mod.y, mod.width, mod.height), 
            mod.base_image
        )
    return view(request, 
        request.user.id if mod.unique_per_user else None, 
        mod.download_file_name,
        *mod.get_view_args())
