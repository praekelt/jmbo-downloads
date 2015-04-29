from django.conf.urls import patterns, url

from downloads.views import ObjectList, download_request


urlpatterns = patterns(
    '',
    # download url
    url(
        r'^$',
        ObjectList.as_view(),
        name='downloads'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        download_request,
        name='download-request'
    ),
)
