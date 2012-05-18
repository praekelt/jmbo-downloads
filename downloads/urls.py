from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from downloads.views import object_list


urlpatterns = patterns('',
    # download url
    url(r'^$', login_required(object_list), {}, name='downloads'),
    url(r'^(?P<file_name>[\w\.-]+)/$', 'downloads.views.download_request',
        name='download_request'),
)
