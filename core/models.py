from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Semester(models.Model):
	title       = models.CharField(max_length=1024)
	start_date  = models.DateField(null=True, blank=True)
	end_date    = models.DateField(null=True, blank=True)
#   members		= [foreign key `semester` in Student]
	
	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
	PHOTOS_DIRECTORY = "profile_photos"

	user 		= models.OneToOneField(User)
	photo		= models.FileField(upload_to=PHOTOS_DIRECTORY, null=True, blank=True)
	semester	= models.ForeignKey(Semester, related_name="members", null=True,
									blank=True, on_delete=models.SET_NULL)
	biography	= models.TextField(null=True, blank=True)

	def __unicode__(self):
		if (self.user.first_name and self.user.last_name):
			return "{0}, {1}".format(self.user.last_name, self.user.first_name)
		else:
			return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
	"""
	Signal for when a user object is created. We want to make sure to create
	a user profile object as well.
	"""
	if (created):
		UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
