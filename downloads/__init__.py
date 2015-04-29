import os
import os.path

from django.conf import settings

from downloads.models import TEMP_UPLOAD_FOLDER


# create temporary downloads folder if it does not exist
tmp_abs_path = os.path.join(settings.MEDIA_ROOT, TEMP_UPLOAD_FOLDER)
if not os.path.exists(tmp_abs_path):
    try:
        os.mkdir(tmp_abs_path, 644)
    except OSError:
        pass
