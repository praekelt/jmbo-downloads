from django.conf.urls.defaults import patterns, url

from downloads.views import object_list, download_request


urlpatterns = patterns(
    '',
    # download url
    url(
        r'^$',
        object_list,
        name='downloads'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        download_request,
        name='download-request'
    ),
)
