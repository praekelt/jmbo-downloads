from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

from downloads.views import object_list, text_overlay


urlpatterns = patterns('',

    # download url
    url(
        r'^$',
        login_required(object_list),
        {},
        name='downloads'
    ),
    url(
        r'^test_image/$',
        text_overlay,
        {"id_number":None, "text":"Awesomeness!"},
    ),
    url(
	r'^(?P<file_name>[\w\.-]+)/$', 
	'downloads.views.download_request',
        {},
    ),
)
