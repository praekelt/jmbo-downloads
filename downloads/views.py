from mimetypes import guess_type

from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.utils.datastructures import SortedDict

from jmbo.generic.views import GenericObjectList

from category.models import Category

from downloads.models import Download


def download_request(request, slug):
    download = Download.permitted.get(slug=slug).as_leaf_class()

    # increment view count
    # contains race condition: download.view_count += 1
    download.view_count = F('view_count') + 1
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


class ObjectList(GenericObjectList):

    def get_extra_context(self, *args, **kwargs):
        dls = list(Download.permitted.all())

        # create dictionary of categories
        cat_dict = SortedDict((id, {'parent': parent, 'title': title, 'items': [],
                              'subcats': [], 'slug': slug, 'child_count': 0})
                for (id, parent, title, slug)
                in Category.objects.values_list('id', 'parent', 'title', 'slug'))
        # add None key for downloads without a category
        cat_dict[None] = {'parent': None, 'items': [], 'child_count': 0, 'subcats': []}
        
        # add downloads to category item lists
        for dl in dls:
            cat_dict[dl.primary_category_id]['items'].append(dl)

        # nest subcategories
        for key, val in cat_dict.items():
            if val['parent']:
                cat_dict[val['parent']]['subcats'].append(key)
            child_count = len(val['items'])
            val['child_count'] += child_count
            if child_count > 0:
                parent_id = val['parent']
                while parent_id:
                    cat_dict[parent_id]['child_count'] += child_count
                    parent_id = cat_dict[parent_id]['parent']              
        
        # remove categories with no items in them
        category_list = []
        for key, val in cat_dict.items():
            subcats = []
            for subcat in val['subcats']:
                if cat_dict[subcat]['child_count'] > 0:
                    subcats.append(cat_dict[subcat])
            val['subcats'] = subcats
            if val['child_count'] > 0 and not val['parent']:
                category_list.append(val)       
        
        return {'title': _('Downloads'), 'category_list': category_list}

    def get_queryset(self, *args, **kwargs):
        return Download.permitted.none()

    def get_paginate_by(self, *args, **kwargs):
        return 20
 
    def get_template_name(self, *args, **kwargs):
        return "downloads/download_list_category.html"

object_list = ObjectList()
