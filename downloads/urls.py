from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    # download url
    url(r'^downloads/(?P<file_id>\d+)/$', 
	'downloads.views.download_request',
        {},
        name='download-request'
    ),
)
