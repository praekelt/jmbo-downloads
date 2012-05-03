from mimetypes import guess_type
from django.utils.encoding import smart_str
from models import Download

def download_request(request, file_slug):
  f = Download.objects.get(slug=file_slug)
  
  mime = guess_type(f.name)
  response = HttpResponse(content_type=mime[0])
  if mime[1]: # check if it has encoding
    respones['Content-Encoding'] = mime[1]
  response['Content-Disposition'] = 'attachment; filename=%s' % f.name
  response['X-Accel-Redirect'] = f.url
  
  return response