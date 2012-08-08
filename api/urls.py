from django.conf.urls import patterns, include, url
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource
from api.handlers import *

comment_resource	= Resource(handler=CommentHandler)
user_resource 		= Resource(handler=UserHandler)

urlpatterns = patterns('',
	url(r'^assignments/add_comment$', comment_resource),
	url(r'^register/check_username$', user_resource)
)
