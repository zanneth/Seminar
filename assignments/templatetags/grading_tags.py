from django import template
from assignments import models
import re

register = template.Library()

@register.simple_tag
def latest_submission_grade(request, assignment):
    profile = request.user.get_profile()
    try:
        latest = models.Submission.objects.filter(submitter=profile, 
                                                assignment=assignment).latest("submitted")
    except models.Submission.DoesNotExist:
        return 0.0

    return latest.points_earned
