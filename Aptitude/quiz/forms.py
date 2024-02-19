from django import forms
from django.contrib.auth.models import User
from . import models

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ('question', 'option1', 'option2', 'option3', 'option4', 'answer')

        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
class ExamForm(forms.ModelForm):
    class Meta:
        model = models.Exam
        fields = ('Exam_name','all_questions','timer','startdate')
