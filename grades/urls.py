from django.conf.urls import patterns, include, url
from grades import views

urlpatterns = patterns('',
	url(r'^$', views.grades, name='grades')
)
