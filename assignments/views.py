from assignments import models
from core.decorators import selected_course_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
@selected_course_required
def assignments(request):
	return render_to_response("assignments.html",
							context_instance=RequestContext(request))
