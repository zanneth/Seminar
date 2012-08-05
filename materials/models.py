from django.db import models
import core.models
import os.path

class MaterialGroup(models.Model):
	title		= models.CharField(max_length=1024)
	course		= models.ForeignKey(core.models.Course, related_name="material_groups")
#	materials	= [foreign key `group` in Material]

	def __unicode__(self):
		return self.title

class Material(models.Model):
	UPLOADS_DIRECTORY = "material_assets"

	file	= models.FileField(upload_to=UPLOADS_DIRECTORY, null=True, blank=True)
	url		= models.URLField(null=True, blank=True)
	name	= models.CharField(max_length=1024, blank=True, null=True)
	created	= models.DateTimeField(auto_now_add=True)
	group	= models.ForeignKey(MaterialGroup, related_name="materials")
	visible	= models.BooleanField(default=True)

	@property
	def basename(self):
		return os.path.basename(self.file.name)

	def __unicode__(self):
		if (self.name):
			return self.name
		elif (self.file):
			return os.path.basename(self.file.name)
		elif (self.url):
			return self.url
		else:
			return "Unknown Material"
