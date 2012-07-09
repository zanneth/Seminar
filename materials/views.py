from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.decorators import selected_course_required

@login_required
@selected_course_required
def materials(request):
	return render_to_response("materials.html",
							context_instance=RequestContext(request))