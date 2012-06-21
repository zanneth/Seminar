from core.decorators import selected_course_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from news import models
import core.models

@selected_course_required
def news(request):
	course = core.models.Course.get_selected_course(request)
	posts = course.news_items.order_by('-created')
	return render_to_response("news.html",
							{ "posts" : posts },
							context_instance=RequestContext(request))

def view_post(request, item_id):
	try:
		post = models.NewsItem.objects.get(pk=item_id)
	except NewsItem.DoesNotExist:
		raise Http404

	return render_to_response("news.html",
							  { "posts" : [post] },
							  context_instance=RequestContext(request))
