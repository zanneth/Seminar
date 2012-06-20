from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Semester(models.Model):
	title       = models.CharField(max_length=1024)
	start_date  = models.DateField(null=True, blank=True)
	end_date    = models.DateField(null=True, blank=True)
#   members		= [foreign key `semester` in Student]
#	courses		= [foreign key `semester` in Course]
	
	def __unicode__(self):
		return self.title


class UserProfile(models.Model):
	PHOTOS_DIRECTORY = "profile_photos"

	user 		= models.OneToOneField(User, editable=False)
	photo		= models.FileField(upload_to=PHOTOS_DIRECTORY, null=True, blank=True)
	semester	= models.ForeignKey(Semester, related_name="members", null=True,
									blank=True, on_delete=models.SET_NULL)
	biography	= models.TextField(null=True, blank=True)
#	courses		= [foreign key `members` in Course]
	default_course = models.ForeignKey("Course", null=True, blank=True)

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


class Course(models.Model):
	ICONS_DIRECTORY = "course_icons"
	SESSION_KEY = "selected_course_id"

	semester	= models.ForeignKey(Semester, related_name="courses", 
									on_delete=models.SET_NULL, null=True, blank=True)
	members		= models.ManyToManyField(UserProfile, null=True, blank=True,
										related_name="courses", through="Membership")
	department	= models.CharField(max_length=100, verbose_name="course department", null=True, blank=True)
	number		= models.CharField(max_length=10, verbose_name="course number", null=True, blank=True)
	name		= models.CharField(max_length=1024)
	section		= models.CharField(max_length=10, verbose_name="section number", null=True, blank=True)
	icon		= models.FileField(upload_to=ICONS_DIRECTORY, null=True, blank=True)

#	news_items	= [foreign key `course` in news.NewsItem]

	def __unicode__(self):
		if (self.department and self.number):
			return "{0}{1} - {2}".format(self.department, self.number, self.name)
		else:
			return self.name

	@staticmethod
	def get_selected_course(request):
		course_id = request.session.get(Course.SESSION_KEY)

		try:
			course = Course.objects.get(pk=course_id)
		except Course.DoesNotExist:
			if (request.session.has_key(Course.SESSION_KEY)):
				del request.session[Course.SESSION_KEY]
			
			if (Course.objects.count() == 1):
				course = Course.objects.all()[0]
			else:
				course = None

		return course

	@staticmethod
	def set_selected_course(request, course_id):
		request.session[Course.SESSION_KEY] = course_id

	@staticmethod
	def clear_selected_course(request):
		del request.session[Course.SESSION_KEY]


class Membership(models.Model):
	USER_TYPES	= (
		(0, "Unknown"),
		(1, "Student"),
		(2, "Auditor"),
		(3, "Teaching Assistant"),
		(4, "Advisor"),
		(5, "Professor")
	)

	member		= models.ForeignKey(UserProfile)
	course		= models.ForeignKey(Course)
	role		= models.IntegerField(choices=USER_TYPES, null=False, blank=False)
