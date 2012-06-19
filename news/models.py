from django.db import models
import core.models
import markdown

class NewsItem(models.Model):
	subject		= models.CharField(max_length=1024)
	author		= models.ForeignKey(core.models.UserProfile, related_name="news_items",
									null=True, blank=True, on_delete=models.SET_NULL)
	created		= models.DateTimeField(auto_now_add=True)
	body		= models.TextField()
	body_html	= models.TextField(editable=False)

	def __unicode__(self):
		return self.subject

	def save(self, force_insert=False, force_update=False):
		self.body_html = markdown.markdown(self.body)
		super(NewsItem, self).save(force_insert, force_update)
