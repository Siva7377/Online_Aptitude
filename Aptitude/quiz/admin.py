from django.contrib import admin
from .models import Question
from .models import Exam

admin.site.register(Question)
admin.site.register(Exam)
