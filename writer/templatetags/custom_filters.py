from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def truncate_words(value, arg):
    length = int(arg)
    words = value.split()
    if len(words) > length:
        return ' '.join(words[:length]) + ' ...'
    else:
        return value
