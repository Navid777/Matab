import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pat_url):
    try:
        pattern = '^' + reverse(pat_url)
    except NoReverseMatch:
        pattern = pat_url
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.filter
def klass(ob):
    return ob.__class__.__name__