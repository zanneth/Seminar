from django.conf.urls import patterns, include, url
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource
from api.handlers import *

comment_resource = Resource(handler=CommentHandler)

urlpatterns = patterns('',
	url(r'^assignments/add_comment$', comment_resource)
)
