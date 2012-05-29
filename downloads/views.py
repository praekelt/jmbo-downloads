from mimetypes import guess_type

from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.db.models import F

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


# traverse up to parent and create absolute category name
def get_full_category(category_id, parent_id, cat_dict):
    if parent_id is not None:  # has parent
        li = cat_dict[category_id]
        li[2] = cat_dict[parent_id][1] + li[2]
        li[3] += 1
        get_full_category(category_id, cat_dict[parent_id][0], cat_dict)


class ObjectList(GenericObjectList):

    def get_extra_context(self, *args, **kwargs):
        dls = list(Download.permitted.filter(do_not_list=False))

        # calculate all absolute category names
        cat_dict = dict((id, [parent, title, title, 1]) for (id, parent, title)
                in Category.objects.values_list('id', 'parent', 'title'))
        for key in cat_dict.keys():
            get_full_category(key, cat_dict[key][0], cat_dict)
        # add None key for downloads without a category
        cat_dict[None] = (None, '', '', 0)

        # perform insertion sort on absolute category name
        for i in range(1, len(dls)):
            val = dls[i]
            j = i - 1
            while j >= 0 and cat_dict[dls[j].primary_category_id][2] > cat_dict[val.primary_category_id][2]:
                dls[j + 1] = dls[j]
                j -= 1
            dls[j + 1] = val

        # construct [(dl_object, depth), ...]
        sorted_list = [(val,
            cat_dict[val.primary_category_id][3]) for val in dls]
        return {'title': _('Downloads'), 'sorted_list': sorted_list}

    def get_queryset(self, *args, **kwargs):
        return Download.permitted.none()

    def get_paginate_by(self, *args, **kwargs):
        return 20

object_list = ObjectList()
