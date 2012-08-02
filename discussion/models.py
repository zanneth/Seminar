from django.db import models
import core.models
import markdown

class DiscussionGroup(models.Model):
	title		= models.CharField(max_length=1024)
	course		= models.ForeignKey(core.models.Course, related_name="discussion_groups")
#	topics		= [foreign key `group` in DiscussionTopic]

	@property
	def ordered_topics(self):
		return self.topics.order_by("-created")

	def __unicode__(self):
		return self.title

class DiscussionTopic(models.Model):
	title		= models.CharField(max_length=1024)
	group		= models.ForeignKey(DiscussionGroup, related_name="topics")
	created		= models.DateTimeField(auto_now_add=True)
	creator		= models.ForeignKey(core.models.UserProfile, related_name="discussion_topics")
#	posts		= [foreign key `topic` in DiscussionPost]

	def __unicode__(self):
		return self.title

class DiscussionPost(models.Model):
	topic		= models.ForeignKey(DiscussionTopic, related_name="posts")
	created		= models.DateTimeField(auto_now_add=True)
	author		= models.ForeignKey(core.models.UserProfile, related_name="discussion_posts")
	body		= models.TextField(null=True, blank=True)
	body_html	= models.TextField(editable=False, null=True, blank=True)

	def save(self, force_insert=False, force_update=False):
		self.body_html = markdown.markdown(self.body)
		super(DiscussionPost, self).save(force_insert, force_update)

	def __unicode__(self):
		return "Discussion Post in {} on {}".format(self.topic, self.created)
