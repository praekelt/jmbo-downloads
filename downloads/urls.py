from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

from downloads.views import all_downloads


urlpatterns = patterns('',

    # download url
    url(
        r'^$',
        login_required(all_downloads),
        {},
        name='downloads'
    ),
    url(
	r'^downloads/(?P<file_name>[\w\.-]+)/$', 
	'downloads.views.download_request',
        {},
    ),
)
