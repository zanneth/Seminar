from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.decorators import selected_course_required
from materials import models
import core.models

@login_required
@selected_course_required
def materials(request):
	course = core.models.Course.get_selected_course(request)
	groups = course.material_groups.all()
	return render_to_response("materials.html",
							{ "material_groups" : groups },
							context_instance=RequestContext(request))