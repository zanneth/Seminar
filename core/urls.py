from django.conf.urls import patterns, include, url
from core import views

urlpatterns = patterns('',
	url(r'^$', views.home, name="home"),
	url(r'^login', views.login, name="login"),
	url(r'^logout', views.logout, name="logout"),
	url(r'^select$', views.select_course, name="select_course"),
	url(r'^select/(?P<course_id>\d+)$', views.select_course),
	url(r'^clear$', views.clear_course, name="clear_course")
)
