from django.contrib import admin
from home.models import Task,Comment, Share
# Register your models here.

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Share)

