from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

from downloads.views import object_list, download_request


urlpatterns = patterns('',

    # download url
    url(
        r'^$',
        login_required(object_list),
        {},
        name='downloads'
    ),
    url(
	r'^(?P<slug>[\w-]+)/$', 
	login_required(download_request),
        {},
    ),
)
