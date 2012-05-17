from django.contrib import admin

from jmbo.admin import ModelBaseAdmin, ModelBaseAdminForm

from downloads.models import Download, TextOverlayImageMod


class DownloadAdminForm(ModelBaseAdminForm):
   class Meta(ModelBaseAdminForm.Meta):
        model = Download

class TOIMAdminForm(ModelBaseAdminForm):
    class Meta(ModelBaseAdminForm.Meta):
        model = TextOverlayImageMod

class DownloadAdmin(ModelBaseAdmin):
    form = DownloadAdminForm
    
    def __init__(self, model, admin_site):
        super(DownloadAdmin, self).__init__(model, admin_site)
        if self.exclude:
            for field in self.exclude:
                try:
                    fields = self.fieldsets[0][1]['fields']
                    i = fields.index(field)
                    self.fieldsets[0][1]['fields'] = fields[0:i] + fields[i+1:]
                except:
                    continue

class ImageModAdmin(DownloadAdmin):
    exclude = ('file',) # file is generated
    
class TextOverlayImageModAdmin(ImageModAdmin):
    form = TOIMAdminForm

    def __init__(self, model, admin_site):
        super(TextOverlayImageModAdmin, self).__init__(model, admin_site)
        one_liners = (('x', 'y', 'width', 'height'), ('font', 'font_size'))
        for line in one_liners:
            for field in line:
                try:
                    fields = self.fieldsets[0][1]['fields']
                    i = fields.index(field)
                    self.fieldsets[0][1]['fields'] = fields[0:i] + fields[i+1:]
                except:
                    continue
        self.fieldsets[0][1]['fields'] += one_liners

    
admin.site.register(Download, DownloadAdmin)
admin.site.register(TextOverlayImageMod, TextOverlayImageModAdmin)
