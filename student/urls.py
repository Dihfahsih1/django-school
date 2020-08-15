from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    # Index Page
    path('', views.index, name='index'),

    # Instructor Page
    path('instructor/', views.InstructorIndexView.as_view(), name='instructor'),

    # Student Pages
    path('student/', views.StudentIndexView.as_view(), name='student'),
    #path('student/add', views.StudentCreate.as_view(), name="student-add"),
    path('student/add', views.student_create, name="student-add"),
    path('student/update/<pk>', views.StudentUpdate.as_view(), name="student-update"),
    path('student/delete/<pk>', views.StudentDelete.as_view(), name="student-delete"),
    path('student/<pk>', views.studentdetail, name='detail'),
    path('student/<pk>/guardian', views.GuardianCreate.as_view(), name='student-guardian'),

    # Enrollment Pages
    path('enroll/', views.EnrollIndexView.as_view(), name='enroll'),
    path('enroll/add', views.EnrollCreate.as_view(), name="enroll-add"),
    path('enroll/update/<pk>', views.EnrollUpdate.as_view(), name="enroll-update"),
    path('enroll/delete/<pk>', views.EnrollDelete.as_view(), name="enroll-delete"),

    # Batch Pages
    path('batch/', views.BatchIndexView.as_view(), name='batch'),
    path('batch/<pk>/students', views.batchstudent, name='batch_student'),
    path('batch/add', views.BatchCreate.as_view(), name='batch-add'),
    path('batch/update/<pk>', views.BatchUpdate.as_view(), name='batch-update'),
    path('batch/delete/<pk>', views.BatchDelete.as_view(), name='batch-delete'),

    # Attendance Pages
    path('attend/', views.AttendanceIndexView.as_view(), name='attend'),
    path('attend/add', views.AttendanceCreate.as_view(), name='attend-add'),
    path('attend/update/<pk>', views.AttendanceUpdate.as_view(), name='attend-update'),
    path('attend/delete/<pk>', views.AttendanceDelete.as_view(), name='attend-delete'),

    # Finance Pages
    path('finance/', views.FinanceIndexView.as_view(), name='finance'),
    path('finance/add', views.FinanceCreate.as_view(), name='finance-add'),
    path('finance/update/<pk>', views.FinanceUpdate.as_view(), name='finance-update'),
    path('finance/delete/<pk>', views.FinanceDelete.as_view(), name='finance-delete'),

    # Report Page
    path('report/', views.monthly_report, name='report'),

    # Progess Page
    path('progress/add/<pk>', views.progress_add, name="progress"),

    # Search Pages
    path('studentsearch/', views.student_search, name="student-search"),
    path('enrollsearch/', views.enroll_search, name="enroll-search"),
    path('attendancesearch/', views.attendance_search, name="attend-search"),
    path('financesearch/', views.finance_search, name="finance-search"),
]