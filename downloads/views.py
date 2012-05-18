from mimetypes import guess_type

from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _

from jmbo.generic.views import GenericObjectList

from downloads.models import Download


def download_request(request, slug): 
    download = Download.permitted.get(slug=slug).as_leaf_class()
    # increment view count
    download.view_count += 1
    download.save()
    
    f, file_name = download.get_file(request)

    mime = guess_type(f.name)
    response = HttpResponse(content_type=mime[0])

    # check if it has encoding
    if mime[1]:
        response['Content-Encoding'] = mime[1]
    response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(file_name)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    response['Pragma'] = 'no-store, no-cache'
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
