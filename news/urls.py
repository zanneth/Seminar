from django.conf.urls import patterns, include, url
from news import views

urlpatterns = patterns('',
	url(r'^$', views.news, name='news'),
	url(r'^(?P<item_id>\d+)$', views.view_post, name='view_post')
)
