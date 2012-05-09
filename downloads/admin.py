from django.contrib import admin

from jmbo.admin import ModelBaseAdmin

from downloads.models import Download


class DownloadAdmin(ModelBaseAdmin):
    pass

admin.site.register(Download, DownloadAdmin)
