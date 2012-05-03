from mimetypes import guess_type

from django.http import HttpResponse
from django.utils.encoding import smart_str

from downloads.models import Download


def download_request(request, file_slug):
  f = Download.objects.get(slug=file_slug).downloadable_file
  
  mime = guess_type(f.name)
  response = HttpResponse(content_type=mime[0])
  
  # check if it has encoding
  if mime[1]:
    respones['Content-Encoding'] = mime[1]
  response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(f.name[f.name.rfind('/')+1:])
  response['Cache-Control'] = 'no-cache'
  response['X-Accel-Redirect'] = smart_str(f.url)
  
  return response