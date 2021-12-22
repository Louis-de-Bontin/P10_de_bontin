from django.contrib import admin
from api import models

admin.site.register(models.User)
admin.site.register(models.Project)
admin.site.register(models.Contributor)
admin.site.register(models.Issue)
admin.site.register(models.Comment)
