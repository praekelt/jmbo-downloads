from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^jmbo/", include("jmbo.urls", namespace="jmbo")),
    url(r"^download/", include("downloads.urls", namespace="downloads")),
    url(r"^comments/", include("django_comments.urls"))
]
