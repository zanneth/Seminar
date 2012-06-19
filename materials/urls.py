from django.conf.urls import patterns, include, url
from materials import views

urlpatterns = patterns('',
	url(r'^$', views.materials, name='materials')
)
