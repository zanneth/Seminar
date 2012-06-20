from core import models
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

def selected_course_required(function=None):
	def _decorator(view_function):
		def _view(request, *args, **kwargs):
			course = models.Course.get_selected_course(request)
			if (course == None):
				return redirect("select_course")
			else:
				return view_function(request, *args, **kwargs)

		return _view

	if (function != None):
		return _decorator(function)
	else:
		return _decorator
