from assignments import models
from core.decorators import selected_course_required
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from pprint import pprint
import calendar
import core.models

@login_required
@selected_course_required
def assignments(request):
	course = core.models.Course.get_selected_course(request)
	assignments = course.assignments.filter(due__gt=datetime.today()).order_by("due")
	cal_html = course.assignment_calendar_html()
	today = date.today()
	return render_to_response("assignments.html",
							{ "assignments"		: assignments,
							  "calendar_html" 	: cal_html,
							  "current_month" 	: today.month,
							  "current_year"	: today.year },
							context_instance=RequestContext(request))

@login_required
def view_assignment(request, assignment_id):
	try:
		assignment = models.Assignment.objects.get(pk=assignment_id)

		if (request.method == "POST" and not assignment.is_past_due):
			submission = models.Submission()
			submission.assignment = assignment
			submission.submitter = request.user.get_profile()
			submission.comments = request.POST.get("comments")
			submission.save()

			for filename in request.FILES.keys():
				submitted_file = request.FILES[filename]
				path = models.SubmissionFile.handle_uploaded_file(submitted_file)
				submission_file = models.SubmissionFile()
				submission_file.file = path
				submission_file.submission = submission
				submission_file.save()

		profile = request.user.get_profile()
		submissions = profile.submissions.filter(assignment=assignment).order_by("-submitted")
	except models.Assignment.DoesNotExist:
		raise Http404

	return render_to_response("view_assignment.html",
							{ "assignment"	: assignment,
							  "submissions" : submissions },
							context_instance=RequestContext(request))

@login_required
@selected_course_required
def calendar(request):
	try:
		year	= int(request.GET["year"])
		month	= int(request.GET["month"])

		caldate = date(year, month, 1)
	except KeyError:
		caldate = date.today()

	course = core.models.Course.get_selected_course(request)
	cal_html = course.assignment_calendar_html(caldate)
	return HttpResponse(cal_html)
