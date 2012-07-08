from django.conf.urls import patterns, include, url
from django.contrib import admin
from seminar import settings
import assignments.views

admin.autodiscover()
urlpatterns = patterns('',
	url(r'^', include('core.urls')),
	url(r'^assignments/', include('assignments.urls')),
	url(r'^discussion/', include('discussion.urls')),
	url(r'^materials/', include('materials.urls')),
	url(r'^news/', include('news.urls')),
	url(r'^grades/', assignments.views.grades, name='grades'),

	url(r'^api/', include('api.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
)
