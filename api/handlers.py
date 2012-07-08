from piston.handler import BaseHandler
from piston.utils import rc
import assignments.models

class CommentHandler(BaseHandler):
	allowed_methods = ("POST",)
	model = assignments.models.Comment

	def create(self, request):
		if (request.user):
			profile = request.user.get_profile()
			body = request.POST.get("body")
			assignment_id = request.POST.get("assignment_id")
			assignment = assignments.models.Assignment.objects.get(pk=assignment_id)

			comment = assignments.models.Comment()
			comment.assignment = assignment
			comment.author = profile
			comment.body = body

			if ("parent_id" in request.POST):
				parent_id = request.POST.get("parent_id")
				parent = assignments.models.Comment.objects.get(pk=parent_id)
				comment.parent = parent

			comment.save()
			return rc.CREATED
		else:
			return rc.FORBIDDEN
