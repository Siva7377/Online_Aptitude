from django.shortcuts import render, redirect, reverse
from . import models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from student import models as SMODEL
from student import forms as SFORM
from django.contrib.auth.models import User
from .forms import QuestionForm
from .forms import ExamForm
from .models import Question


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'quiz/index.html')


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_student(request.user):
        return redirect('student/student-dashboard')
    else:
        return redirect('admin-dashboard')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
        'total_question': models.Question.objects.all().count(),
    }
    return render(request, 'quiz/admin_dashboard.html', context=dict)


@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
    }
    return render(request, 'quiz/admin_student.html', context=dict)


@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students = SMODEL.Student.objects.all()
    return render(request, 'quiz/admin_view_student.html', {'students': students})


@login_required(login_url='adminlogin')
def update_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = SMODEL.User.objects.get(id=student.user_id)
    userForm = SFORM.StudentUserForm(instance=user)
    studentForm = SFORM.StudentForm(request.FILES, instance=student)
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = SFORM.StudentUserForm(request.POST, instance=user)
        studentForm = SFORM.StudentForm(request.POST, request.FILES, instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request, 'quiz/update_student.html', context=mydict)


@login_required(login_url='adminlogin')
def delete_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request, 'quiz/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    submitted = False
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            submitted = True
            return render(request, 'quiz/admin_add_question.html', {'submitted': submitted})
    else:
        form = QuestionForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'quiz/admin_add_question.html', {'form': form, 'submitted': submitted})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    questions = models.Question.objects.all()
    return render(request, 'quiz/admin_view_question.html', {'questions': questions})


@login_required(login_url='adminlogin')
def admin_exam_view(request):
    return render(request, 'quiz/admin_exam.html')


@login_required(login_url='adminlogin')
def admin_create_exam(request):
    submitted = False
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            submitted = True
            return render(request, 'quiz/create_exam.html', {'submitted': submitted})
    else:
        form = ExamForm
        if 'submitted' in request.GET:
            submitted = True
        return render(request, 'quiz/create_exam.html', {'form': form, 'submitted': submitted})


@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students = SMODEL.Student.objects.all()
    return render(request, 'quiz/admin_view_student_marks.html', {'students': students})


def admin_view_score(request, pk):
    exam = models.Exam.objects.all()
    response = render(request, 'quiz/view-score.html', {'exam': exam})
    response.set_cookie('student_id', str(pk))
    return response


def view_test_score(request, pk):
    exam = models.Exam.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    # print(exam)
    # print(student_id)
    # student = SMODEL.Student.objects.get(id=student_id)
    # print(student)
    results = models.Result.objects.all().filter(exam=exam).filter(user_id=student_id)
    return render(request, 'quiz/view_test_score.html', {'results': results})
