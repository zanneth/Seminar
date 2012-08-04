from django.conf.urls import patterns, include, url
from discussion import views

urlpatterns = patterns('',
	url(r'^$', views.discussion, name="discussion"),
	url(r'^delete/(?P<post_id>\d+)$', views.delete_post, name="delete_post"),

	url(r'^(?P<group_name_url_form>.+)/(?P<topic_id>\d+)$', views.view_topic, name="view_topic"),
	url(r'^(?P<group_name_url_form>.+)/new$', views.new_topic, name="new_topic"),
	url(r'^(?P<group_name_url_form>.+)/$', views.view_group, name="view_group")
)
