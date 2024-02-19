from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from pytz import utc
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from quiz import models as QMODEL
from .models import Student


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'student/studentclick.html')


def student_signup_view(request):
    userForm = forms.StudentUserForm()
    studentForm = forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = forms.StudentUserForm(request.POST)
        studentForm = forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request, 'student/studentsignup.html', context=mydict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict = {

        'total_Exam': QMODEL.Exam.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
    }
    return render(request, 'student/student_dashboard.html', context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    exam=QMODEL.Exam.objects.all()
    return render(request,'student/student_exam.html',{'exam':exam})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    exam = QMODEL.Exam.objects.get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(exam=exam).count()
    total_marks = total_questions
    results = QMODEL.Result.objects.all().filter(exam=exam)
    k = 0
    student = request.user.id
    print("current id: ",student)

    for i in results:
        print("student2",i.user_id)
        if student == i.user_id:
            k += 1

    # print(k)
    # current_time = time.localtime()
    # c_time = time.strftime('%d %b %Y %H:%M:%S', current_time)

    c_time = datetime.datetime.now()
    st_date= exam.startdate

    print(c_time.replace(tzinfo=utc))
    print(c_time)
    print(st_date.replace(tzinfo=utc))
    print(st_date)

    enable = True
    if c_time.replace(tzinfo=utc) < st_date.replace(tzinfo=utc):
        enable = False

    return render(request, 'student/take_exam.html',{'exam': exam, 'total_questions': total_questions, 'total_marks': total_marks,'results':results,'k':k,"time":c_time,"enable":enable})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam(request,pk):
    exam = QMODEL.Exam.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(exam=exam)

    response = render(request,'student/start_exam.html',{'exam': exam,'questions': questions,})
    response.set_cookie('exam_id', exam.id)
    return response

@login_required(login_url = 'studentlogin')
@user_passes_test(is_student)
@csrf_exempt
def calculate_marks_view(request):
    if request.method == 'POST':
        if request.COOKIES.get('exam_id') is not None:
            response = render(request, 'student/aftersubmit.html')
            exam_id = request.COOKIES.get('exam_id')
            exam = QMODEL.Exam.objects.get(id=exam_id)
            total_marks = 0
            questions = QMODEL.Question.objects.all().filter(exam=exam)
            for i in range(len(questions)):
                k = str(i+1)
                selected_ans = request.COOKIES.get(str(i + 1))
                #print(selected_ans)
                actual_answer = questions[i].answer
                if selected_ans == actual_answer:
                    total_marks = total_marks + 1
                response.delete_cookie(k)
            user = request.user
            student = models.Student.objects.get(user_id=request.user.id)
            result = QMODEL.Result()
            result.marks = total_marks
            result.exam = exam
            result.user = user
            result.student = student
            result.save()
            return response