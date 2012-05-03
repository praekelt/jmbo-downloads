from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',

    # download url
    url(
	r'^(?P<file_slug>[\w-]+)/$', 
	'downloads.views.download_request',
        {},
    ),
)
