from core import models

def courses(request):
	selected_course = models.Course.get_selected_course(request)
	return { 
		"selected_course" : selected_course,
		"other_courses_available" : (models.Course.objects.count() > 1)
	}
