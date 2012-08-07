from assignments import models
from core.decorators import selected_course_required, superstudent_required
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
@selected_course_required
def grades(request):
	course = core.models.Course.get_selected_course(request)
	groups = course.assignment_groups.all()
	ungrouped = course.assignments.filter(group=None)
	return render_to_response("grades.html",
							{ "assignment_groups"		: groups,
							  "ungrouped_assignments"	: ungrouped },
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
		has_visible_submissions = profile.submissions.filter(assignment=assignment, visible=True).count()
		comments = assignment.comments.order_by("created")
	except models.Assignment.DoesNotExist:
		raise Http404

	return render_to_response("view_assignment.html",
							{ "assignment"	: assignment,
							  "submissions" : submissions,
							  "has_visible_submissions" : has_visible_submissions,
							  "comments"	: comments },
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

@login_required
@selected_course_required
@superstudent_required
def teacher(request):
	course = core.models.Course.get_selected_course(request)
	assignment_groups = course.assignment_groups.order_by("title")

	return render_to_response("teacher.html",
							{ "assignment_groups" : assignment_groups },
							context_instance=RequestContext(request))

@login_required
@superstudent_required
def view_submissions(request, assignment_id):
	try:
		assignment = models.Assignment.objects.get(pk=assignment_id)
	except models.Assignment.DoesNotExist:
		return Http404

	course = core.models.Course.get_selected_course(request)
	members = course.members.order_by("user__last_name")
	members_submissions = []
	for member in members:
		submissions = member.submissions.filter(assignment=assignment).order_by("-submitted")
		members_submissions.append( (member, submissions) )

	return render_to_response("view_submissions.html",
							{ "assignment"			: assignment,
							  "members_submissions"	: members_submissions },
							context_instance=RequestContext(request))

@login_required
@superstudent_required
def view_submission(request, submission_id):
	try:
		submission = models.Submission.objects.get(pk=submission_id)
	except models.Submission.DoesNotExist:
		return Http404

	if (request.method == "POST"):
		points = request.POST.get("points_earned")
		submission.points_earned = points
		submission.save()

	return render_to_response("view_submission.html",
							{ "submission" : submission },
							context_instance=RequestContext(request))
