from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def noescape(value):
    """
    Disables autoescaping for a string.
    """
    return mark_safe(value)
