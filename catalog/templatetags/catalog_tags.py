import datetime
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.filter(name='check_foto')
def check_foto(value, obj_item):
    if obj_item.image.name != '':
        return obj_item.image.url
    else:
        return f"{settings.MEDIA_URL}products/no_foto.jpg"
