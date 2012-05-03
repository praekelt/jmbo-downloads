from django.contrib import admin

from jmbo.admin import ModelBaseAdmin

from downloads.models import Download


admin.site.register(Download, ModelBaseAdmin)
