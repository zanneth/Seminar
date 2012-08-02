from bs4 import BeautifulSoup
from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import calendar
import markdown
import re

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
#	submissions = [foreign key `submitter` in assignments.Submission]
#	comments	= [foreign key `author` in assignments.Comment]
#	discussion_topics = [foreign key `creator` in discussion.DiscussionPost]

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
	description = models.TextField(null=True, blank=True)
	description_html = models.TextField(editable=False, null=True, blank=True)

#	news_items	= [foreign key `course` in news.NewsItem]
#	assignment_groups = [foreign key `course` in assignments.AssignmentGroup]
#	assignments	= [foreign key `course` in assignments.Assignment]
#	material_groups = [foreign key `course` in materials.MaterialGroup]
#	discussion_topics = [foreign key `course` in discussion.DiscussionTopic]

	def __unicode__(self):
		if (self.department and self.number):
			return "{0}{1} - {2}".format(self.department, self.number, self.name)
		else:
			return self.name

	def save(self, force_insert=False, force_update=False):
		self.description_html = markdown.markdown(self.description)
		super(Course, self).save(force_insert, force_update)

	def assignment_calendar_html(self, date=date.today()):
		"""
		Returns an assignment calendar html string for the course according to 
		the specified month and year.
		"""
		assgn_cal_item_class = "assignment-calendar-item"

		try:
			cal = calendar.HTMLCalendar()
			cal_html = cal.formatmonth(date.year, date.month)

			# We need to modify the DOM to add the assignment calendar items
			soup = BeautifulSoup(cal_html)
			day_cells = soup.find_all("td", {"class" : re.compile(r"mon|tue|wed|thu|fri|sat|sun")})
			assignments = self.assignments.filter(due__year=date.year, due__month=date.month)
			for assignment in assignments:
				day_due = int(assignment.due.day)
				if (day_due < len(day_cells)):
					cell = day_cells[day_due - 1]
					items_element = cell.find("div", { "class" : assgn_cal_item_class })
					if (not items_element):
						items_element = soup.new_tag("div", **{ "class" : assgn_cal_item_class })
						cell.append(items_element)

					priority = assignment.priority_string()
					tag = soup.new_tag("span", **{ "class" : priority })
					tag.string = "&#8226;"
					items_element.append(tag)

			today = date.today()
			if (date.month == today.month and today.day < len(day_cells)):
				day_cells[today.day - 1]["id"] = "today";

			return str(soup)
		except (AttributeError, TypeError):
			raise AssertionError("Input date should be a `date` object.")

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

	def __unicode__(self):
		role_name = self.USER_TYPES[self.role][1]
		return "{0} ({1}) in {2}".format(self.member, role_name, self.course)
