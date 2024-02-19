"""aptitude URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from quiz import views
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls')),

    path('', views.home_view, name=''),
    path('logout', LogoutView.as_view(template_name='quiz/logout.html'), name='logout'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='quiz/adminlogin.html'), name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),

    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),

    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),

    path('admin-exam', views.admin_exam_view,name='admin-exam'),
    path('create-exam',views.admin_create_exam,name='create-exam'),

    path('admin-question', views.admin_question_view,name='admin-question'),
    path('admin-add-question', views.admin_add_question_view,name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,name='admin-view-question'),

    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),

    path('admin-view-student-marks', views.admin_view_student_marks_view,name='admin-view-student-marks'),
    path('view-score/<int:pk>', views.admin_view_score,name='view-score'),
    path('view-test-score/<int:pk>',views.view_test_score,name='view-test-score'),

]