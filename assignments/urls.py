from assignments import views
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', views.assignments, name='assignments'),
	url(r'^calendar\.html', views.calendar, name="assignments_calendar")
)