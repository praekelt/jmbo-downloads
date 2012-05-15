from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

from downloads.views import object_list, image_mod, download_request


urlpatterns = patterns('',

    # download url
    url(
        r'^$',
        login_required(object_list),
        {},
        name='downloads'
    ),
    url(
        r'^image-mod/(?P<slug>[\w-]+)$',
        login_required(image_mod),
        {},
    ),
    url(
	r'^(?P<file_name>[\w\.-]+)/$', 
	login_required(download_request),
        {},
    ),
)
