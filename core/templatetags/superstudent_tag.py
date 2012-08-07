from django import template
from core import models

register = template.Library()

@register.assignment_tag
def superstudent_status(request):
    """
    Returns whether or not the currently logged in user is a superstudent or not.
    """
    user = request.user.get_profile()
    course = models.Course.get_selected_course(request)
    return user.is_superstudent(course)
