from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def active_url(request, path_name, *args, **kwargs):
    try:
        url = reverse(path_name, args=args, kwargs=kwargs)
        if url == request.path:
            return 'active'
    except NoReverseMatch:
        pass
    return ''

