from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def materials(request):
	return render_to_response("home.html",
							context_instance=RequestContext(request))