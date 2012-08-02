from django.contrib import admin
from discussion import models

admin.site.register(models.DiscussionGroup)
admin.site.register(models.DiscussionTopic)
admin.site.register(models.DiscussionPost)
