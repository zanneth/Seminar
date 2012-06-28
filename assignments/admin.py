from django.contrib import admin
from assignments import models

admin.site.register(models.AssignmentGroup)
admin.site.register(models.Assignment)
admin.site.register(models.Asset)
admin.site.register(models.Submission)
admin.site.register(models.SubmissionFile)
