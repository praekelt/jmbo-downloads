from django.dispatch import Signal


# allows other apps to track downloads
download_requested = Signal(
    providing_args=['request']
)
