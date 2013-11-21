import re

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _

from south.modelsinspector import add_introspection_rules


class ColourField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        kwargs['help_text'] = "Hexadecimal format, e.g. #f0d245"
        super(ColourField, self).__init__(*args, **kwargs)

    def formfield(self, *args, **kwargs):
        kwargs['validators'] = [
            RegexValidator(r'^#[\da-f]{6}$',
                           _(u'Enter a hexadecimal-format colour.'),
                           'Invalid')
        ]
        return super(ColourField, self).formfield(*args, **kwargs)


add_introspection_rules([], ["^downloads\.fields\.ColourField"])
