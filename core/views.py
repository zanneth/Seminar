from core.decorators import selected_course_required
from core import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
import news.models
from pprint import pprint

def login(request):
	UNKNOWN_ERROR = (0, "An unknown error occurred.")
	INVALID_CREDENTIALS_ERROR = (1, "Invalid username or password.")
	ACCOUNT_DISABLED_ERROR = (2, "Account disabled. Please contact an administrator for more information.")

	error = None
	if (request.POST):
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = auth.authenticate(username=username, password=password)
		if (user != None):
			if (user.is_active):
				auth.login(request, user)
				return redirect("home")
			else:
				error = ACCOUNT_DISABLED_ERROR
		else:
			error = INVALID_CREDENTIALS_ERROR

	return render_to_response("login.html",
							{ "error" : error },
							context_instance=RequestContext(request))

def logout(request):
	auth.logout(request)
	return redirect("home")

def select_course(request, course_id=None):
	if (course_id != None):
		models.Course.set_selected_course(request, course_id)
		return redirect("home")

	courses = models.Course.objects.all()
	return render_to_response("select_course.html",
							{ "courses" : courses },
							context_instance=RequestContext(request))

@selected_course_required
def clear_course(request):
	models.Course.clear_selected_course(request)
	return redirect("home")

@selected_course_required
def home(request):
	selected_course = models.Course.get_selected_course(request)
	recent_news = selected_course.news_items.order_by("-created")
	return render_to_response("home.html",
							{ "recent_news" : recent_news },
							context_instance=RequestContext(request))
