from django.conf.urls import url

from downloads.views import ObjectList, download_request


urlpatterns = [
    url(
        r"^$",
        ObjectList.as_view(),
        name="downloads"
    ),
    url(
        r"^(?P<slug>[\w-]+)/$",
        download_request,
        name="download-request"
    )
]
