from django import template
from django.db.models import Q
from assignments import models
import re

register = template.Library()

@register.simple_tag
def latest_submission_grade(request, assignment):
    profile = request.user.get_profile()
    try:
        latest = models.Submission.objects.filter(submitter=profile, assignment=assignment)
        latest = latest.filter(~Q(points_earned=None)).latest("submitted")
    except models.Submission.DoesNotExist:
        return 0.0

    return latest.points_earned

@register.assignment_tag
def weight_for_assignment(request, assignment):
	group = assignment.group
	grade = latest_submission_grade(request, assignment)
	if (group):
		total_weight = group.weight / group.assignments.count()
		weighted_grade = (grade / assignment.max_points) * total_weight
		return (weighted_grade, total_weight)
	elif (grade != None):
		return (grade, 0.0)
	else:
		return (0.0, 0.0)

@register.assignment_tag
def weight_for_group(request, group):
	total_weight = group.weight
	total_weighted_score = 0.0
	assignment_weight = total_weight / group.assignments.count()

	for assignment in group.assignments.all():
		grade = latest_submission_grade(request, assignment)
		if (grade == None):
			grade = 0.0
		weighted_grade = (grade / assignment.max_points) * assignment_weight
		total_weighted_score += weighted_grade

	return (total_weighted_score, total_weight)
