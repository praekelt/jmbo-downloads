from django.contrib import admin

from jmbo.admin import ModelBaseAdmin

from downloads.models import Download, TextOverlayImageMod


class DownloadAdmin(ModelBaseAdmin):
    pass


class ImageModAdmin(ModelBaseAdmin):
    pass

    
admin.site.register(Download, DownloadAdmin)
admin.site.register(TextOverlayImageMod, ImageModAdmin)
