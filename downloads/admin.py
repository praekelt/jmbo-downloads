from django.contrib import admin
from django.db.models.query import QuerySet

from jmbo.admin import ModelBaseAdmin, ModelBaseAdminForm

from downloads.models import Download, TextOverlayTemporaryDownload


class DownloadAdminForm(ModelBaseAdminForm):
    class Meta(ModelBaseAdminForm.Meta):
        model = Download


class TOIMAdminForm(ModelBaseAdminForm):
    class Meta(ModelBaseAdminForm.Meta):
        model = TextOverlayTemporaryDownload


class DownloadAdmin(ModelBaseAdmin):
    form = DownloadAdminForm

    def __init__(self, model, admin_site):
        super(DownloadAdmin, self).__init__(model, admin_site)
        # add the number of downloads to Jmbo's default list display
        self.list_display += ('view_count',)
        # magic that should go into ModelBaseAdmin at later stage
        if self.exclude:
            for field in self.exclude:
                try:
                    fields = self.fieldsets[0][1]['fields']
                    i = fields.index(field)
                    self.fieldsets[0][1]['fields'] = fields[0:i] + \
                        fields[i + 1:]
                except:
                    continue

    def queryset(self, request):
        qs = super(DownloadAdmin, self).queryset(request)
        pks = set()
        for obj in qs:
            if obj.__class__ is obj.as_leaf_class().__class__:
                pks.add(obj.pk)
        return qs.filter(pk__in=pks)


class ImageModAdmin(DownloadAdmin):
    exclude = ('file',)  # file is generated


class TextOverlayImageModAdmin(ImageModAdmin):
    form = TOIMAdminForm

    def __init__(self, model, admin_site):
        super(TextOverlayImageModAdmin, self).__init__(model, admin_site)
        one_liners = (('x', 'y', 'width', 'height'), ('font', 'font_size'))
        # magic that should go into ModelBaseAdmin at later stage
        for line in one_liners:
            for field in line:
                try:
                    fields = self.fieldsets[0][1]['fields']
                    i = fields.index(field)
                    self.fieldsets[0][1]['fields'] = fields[0:i] + \
                        fields[i + 1:]
                except:
                    continue
        self.fieldsets[0][1]['fields'] += one_liners


admin.site.register(Download, DownloadAdmin)
admin.site.register(TextOverlayTemporaryDownload, TextOverlayImageModAdmin)
