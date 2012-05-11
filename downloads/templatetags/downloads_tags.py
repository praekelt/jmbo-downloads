from django import template

register = template.Library()


@register.inclusion_tag('downloads/inclusion_tags/download_detail.html')
def download_detail(obj, request):
    return {'object': obj, 'request': request}