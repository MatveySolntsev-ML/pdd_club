from django.contrib import admin

from .models import Comment, Question, Topic

admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Comment)
