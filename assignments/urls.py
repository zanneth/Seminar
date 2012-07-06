from assignments import views
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', views.assignments, name='assignments'),
	url(r'^(?P<assignment_id>\d+)', views.view_assignment, name='view_assignment'),
	url(r'^calendar\.html', views.calendar, name="assignments_calendar")
)
