from jmbo.managers import PermittedManager


# manager that excludes invisible downloads by default
class VisibleManager(PermittedManager):

    def get_queryset(self, include_invisible=False):
        qs = super(VisibleManager, self).get_queryset()
        if not include_invisible:
            qs = qs.exclude(visible=False)
        return qs
