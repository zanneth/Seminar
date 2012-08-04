from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render_to_response
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
@selected_course_required
def view_group(request, group_name_url_form):
	selected_group = models.DiscussionGroup.reverse_url_form(group_name_url_form)
	if (selected_group == None):
		raise Http404

	return render_to_response("discussion.html",
							{ "discussion_groups" : [selected_group] },
							context_instance=RequestContext(request))

@login_required
def view_topic(request, group_name_url_form, topic_id):
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

@login_required
@selected_course_required
def new_topic(request, group_name_url_form):
	group = models.DiscussionGroup.reverse_url_form(group_name_url_form)
	if (group == None):
		raise Http404

	if (request.method == "POST"):
		title = request.POST.get("topic_title")
		body = request.POST.get("topic_body")
		author = request.user.get_profile()

		topic = models.DiscussionTopic()
		topic.title = title
		topic.group = group
		topic.creator = author
		topic.save()

		post = models.DiscussionPost()
		post.topic = topic
		post.author = author
		post.body = body
		post.save()

		return redirect("view_topic", group_name_url_form=group.url_form, topic_id=topic.pk)

	return render_to_response("new_topic.html",
							{ "discussion_group" : group },
							context_instance=RequestContext(request))

@login_required
def delete_post(request, post_id):
	topic_deleted = False
	try:
		post = models.DiscussionPost.objects.get(pk=post_id)
		if (post.author.user != request.user):
			return HttpResponse('Unauthorized', status=401)

		if (post.topic.posts.order_by("created")[0] == post):
			post.topic.delete()
			topic_deleted = True

		post.delete()
	except models.DiscussionPost.DoesNotExist:
		raise Http404

	if (topic_deleted):
		return redirect("discussion")

	return redirect("view_topic", group_name_url_form=post.topic.group.url_form, topic_id=post.topic.pk)
