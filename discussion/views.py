from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.decorators import selected_course_required
from discussion import models
import core.models

@login_required
@selected_course_required
def discussion(request):
	course = core.models.Course.get_selected_course(request)
	groups = course.discussion_groups.order_by("title")
	return render_to_response("discussion.html",
						{ "discussion_groups" : groups },
						context_instance=RequestContext(request))

@login_required
def view_topic(request, topic_id):
	try:
		topic = models.DiscussionTopic.objects.get(pk=topic_id)
	except models.DiscussionTopic.DoesNotExist:
		raise Http404

	if (request.method == "POST"):
		body = request.POST.get("body")

		if (body and len(body) > 0):
			post = models.DiscussionPost()
			post.author = request.user.get_profile()
			post.body = request.POST.get("body")
			post.topic = topic
			post.save()

	posts = topic.posts.order_by("created")
	return render_to_response("view_topic.html",
							{ "topic"	: topic,
							  "posts"	: posts },
							context_instance=RequestContext(request))
