from assignments import models
from core.decorators import selected_course_required
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
import calendar

@login_required
@selected_course_required
def assignments(request):
	today = datetime.today()
	cal = calendar.HTMLCalendar()
	cal_html = cal.formatmonth(today.year, today.month)
	return render_to_response("assignments.html",
							{ "calendar_html" : cal_html },
							context_instance=RequestContext(request))
