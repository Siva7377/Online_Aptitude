import datetime

from django.contrib.auth.models import User
from django.db import models

from django.db import models
from datetime import time
from student.models import Student


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=200, choices=cat)

    def __str__(self):
        return self.question


class Exam(models.Model):
    Exam_name = models.CharField(max_length=50, unique=True)
    all_questions = models.ManyToManyField(Question, blank=True)
    timer = models.IntegerField(blank=False, help_text="Enter only  minutes")
    startdate = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.Exam_name


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
