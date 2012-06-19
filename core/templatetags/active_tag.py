from django import template
import re

register = template.Library()

@register.simple_tag
def active(request, pattern):
    """
    Returns whether or not the navigation item specified by 'pattern' matches
    the current request. Currently used in highlighting currently active tab.
    """
    
    if pattern == '/' and request.path == '/':
        return 'active'
    elif pattern != '/' and re.search(pattern, request.path):
        return 'active'
    else:
        return 'inactive'
    