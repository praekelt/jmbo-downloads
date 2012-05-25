from mimetypes import guess_type

from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

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
    response['Content-Disposition'] = 'attachment; \
        filename="%s"' % smart_str(file_name)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    response['Pragma'] = 'no-store, no-cache'
    response['X-Accel-Redirect'] = smart_str(f.url)

    return response


def get_full_category(category, full_name):
    if not category:
        return full_name
    else:
        return get_full_category(category.parent, category.title + full_name)


class ObjectList(GenericObjectList):

    def get_extra_context(self, *args, **kwargs):
        dls = Download.permitted.all()
        # re-order hierarchically
        sort_list = []
        index = 0
        cat = None
        full_cat = ''
        for dl in dls:
            if dl.primary_category != cat:
                cat = dl.primary_category
                full_cat = get_full_category(cat, '')
            sort_list.append((full_cat, index))
            index += 1
        # perform insertion sort on full category name
        for i in range(1, len(sort_list)):
            val = sort_list[i]
            j = i - 1
            while j >= 0 and sort_list[j][0] > val[0]:
                sort_list[j + 1] = sort_list[j]
                j -= 1
            sort_list[j + 1] = val
        sorted_dls = []
        for tup in sort_list:
            sorted_dls.append(dls[tup[1]])
        return {'title': _('Downloads'), 'sorted_list':sorted_dls}
    
    def get_queryset(self, *args, **kwargs):
        return Download.permitted.none()

    def get_paginate_by(self, *args, **kwargs):
        return 20

object_list = ObjectList()
