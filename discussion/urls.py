from django.conf.urls import patterns, include, url
from discussion import views

urlpatterns = patterns('',
	url(r'^$', views.discussion, name='discussion')
)
