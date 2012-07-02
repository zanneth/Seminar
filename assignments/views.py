from assignments import models
from core.decorators import selected_course_required
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
import calendar
import core.models

@login_required
@selected_course_required
def assignments(request):
	course = core.models.Course.get_selected_course(request)
	cal_html = course.assignment_calendar_html()
	return render_to_response("assignments.html",
							{ "calendar_html" : cal_html },
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
