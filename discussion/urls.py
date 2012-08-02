from django.conf.urls import patterns, include, url
from discussion import views

urlpatterns = patterns('',
	url(r'^$', views.discussion, name='discussion'),
	url(r'^(?P<topic_id>\d+)$', views.view_topic, name="view_topic")
)
