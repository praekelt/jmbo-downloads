from mimetypes import guess_type
from django.utils.encoding import smart_str

def download_request(request, file_id):
  pathname = smart_str(path_map[file_id])
  index = pathname.rfind('/') 
  filename = pathname[index + 1:] if index > -1 else pathname
  
  mime = guess_type(filename)
  response = HttpResponse(content_type=mime[0])
  if mime[1]: # check if it has encoding
    respones['Content-Encoding'] = mime[1]
  response['Content-Disposition'] = 'attachment; filename=%s' % filename
  response['X-Accel-Redirect'] = pathname
  
  return response