__author__ = 'David'

from django import template
from django.shortcuts import resolve_url

register = template.Library()


@register.simple_tag
def active(request, url):

    pattern = resolve_url(url)

    if pattern == request.path:
        return 'active'
    return ''

@register.simple_tag
def has_error(error):
    if error:
        return 'has-error has-feedback'

    return ''

# @register.simple_tag
# def panel_error(form, fields):
#     panel_class = 'panel-default'
#
#     i = 0
#     for f in fields:
#         if i > 0:
#             if getattr(form, f).errors:
#                 panel_class = 'panel-danger'
#
#         i += 1
#
#     return panel_class