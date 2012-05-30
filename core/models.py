from django.db import models

class Semester(models.Model):
	title       = models.CharField(max_length=1024)
	start_date  = models.DateField(null=True, blank=True)
	end_date    = models.DateField(null=True, blank=True)
#   students	= [foreign key `semester` in Student]
	
	def __unicode__(self):
		return self.title

class Student(models.Model):
	PHOTOS_DIRECTORY = "student_photos"

	name		= models.CharField(max_length=1024)
	email		= models.EmailField(null=True, blank=True)
	photo		= models.FileField(upload_to=PHOTOS_DIRECTORY, null=True, blank=True)
	semester	= models.ForeignKey(Semester, related_name="students", null=True,
									blank=True, on_delete=models.SET_NULL)
	biography	= models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name
