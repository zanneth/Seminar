from datetime import date, datetime, timedelta
from django.db import models
from django.utils import timezone
from random import random
from seminar import settings
import core.models
import markdown
import os.path

class AssignmentGroup(models.Model):
	title		= models.CharField(max_length=1024)
	weight		= models.FloatField(blank=True, default=0.0)
#	assignments = [foreign key `group` in Assignment]
	
	def __unicode__(self):
		return self.title


class Assignment(models.Model):
	PRIORITIES = (
		(0, "Low"),
		(1, "Normal"),
		(2, "High")
	)

	today = datetime.today()
	tomorrow = datetime(today.year, today.month, today.day, 23, 59)
	tomorrow += timedelta(days=1)

	course		= models.ForeignKey(core.models.Course, related_name="assignments")
	title		= models.CharField(max_length=1024)
	description = models.TextField(null=True, blank=True)
	description_html = models.TextField(editable=False)
	group		= models.ForeignKey(AssignmentGroup, null=True, blank=True, related_name="assignments")
	created		= models.DateTimeField(auto_now_add=True)
	due			= models.DateTimeField(null=True, blank=True, default=tomorrow)
	max_points	= models.FloatField()
	allows_submissions = models.BooleanField(default=True)
	priority	= models.IntegerField(choices=PRIORITIES, default=1)
	visible		= models.BooleanField(default=True)

#	submissions = [foreign key `assignment` in Submission]
#	assets		= [foreign key `assignment` in Asset]
	
	def __unicode__(self):
		return self.title

	def save(self, force_insert=False, force_update=False):
		self.description_html = markdown.markdown(self.description)
		super(Assignment, self).save(force_insert, force_update)

	def priority_string(self):
		return self.PRIORITIES[self.priority][1].lower()

	@property
	def is_past_due(self):
		tz = timezone.get_current_timezone()
		return bool(datetime.now(tz) > self.due)

class Asset(models.Model):
	UPLOADS_DIRECTORY = "assignment_assets"

	file		= models.FileField(upload_to=UPLOADS_DIRECTORY)
	name		= models.CharField(max_length=1024, null=True, blank=True)
	created		= models.DateTimeField(auto_now_add=True)
	assignment	= models.ForeignKey(Assignment, related_name="assets")

	def __unicode__(self):
		if (self.name):
			return self.name
		else:
			return os.path.basename(self.file.name)


class Submission(models.Model):
	assignment		= models.ForeignKey(Assignment, related_name="submissions")
	submitter		= models.ForeignKey(core.models.UserProfile, related_name="submissions")
	submitted		= models.DateTimeField(auto_now_add=True)
	comments		= models.TextField(blank=True)
#	files			= [foreign key `submission` in SubmissionFile]
	points_earned	= models.FloatField(blank=True, null=True)


class SubmissionFile(models.Model):
	UPLOADS_DIRECTORY = "assignment_submissions"

	file		= models.FileField(upload_to=UPLOADS_DIRECTORY)
	created		= models.DateTimeField(auto_now_add=True)
	submission	= models.ForeignKey(Submission, related_name="files")

	def __unicode__(self):
		return os.path.basename(self.file.name)

	@staticmethod
	def handle_uploaded_file(f):
		basename = os.path.basename(f.name)
		dest_dir = os.path.join(settings.MEDIA_ROOT, SubmissionFile.UPLOADS_DIRECTORY)
		dest_path = os.path.join(dest_dir, basename)
		if (os.path.isfile(dest_path)):
			split_name = os.path.splitext(basename)
			new_name = "{0}_{1}{2}".format(split_name[0], int(random()*100), split_name[1])
			dest_path = os.path.join(dest_dir, new_name)

		with open(dest_path, "wb+") as destination:
			for chunk in f.chunks():
				destination.write(chunk)

		return dest_path
