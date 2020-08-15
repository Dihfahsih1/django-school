from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Instructor, Student, Attendance, Progress, Fee, Batch, Enrollment, Guardian
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from functools import reduce

from datetime import datetime
from django.db.models import Sum

from .form import *

# Index Page
def index(request):
    instructor = Instructor.objects.get(id=1)
    return render(request, 'student/index.html', context={'instructor': instructor})

# Instructor Page
class InstructorIndexView(generic.ListView):
    template_name = 'student/instructor.html'

    def get_queryset(self):
        return Instructor.objects.all()
        
# Student Index Page
class StudentIndexView(generic.ListView):
    template_name = 'student/student.html'

    def get_queryset(self):
        return Student.objects.all()

# Student Detail Page
def studentdetail(request, pk):
    student_detail = Student.objects.get(pk=pk)
    guardian_detail = student_detail.guardian
    attendance_detail = Attendance.objects.filter(student=pk)
    progress_detail = Progress.objects.filter(student=pk)
    fee_detail = Fee.objects.filter(student=pk)
    context = {
        'stu': student_detail,
        'guardian': guardian_detail,
        'attendance': attendance_detail,
        'progress':  progress_detail,
        'fee': fee_detail,
    }
    return render(request, 'student/detail.html', context)

# Student Update Pages
# class StudentCreate(CreateView):
#     model = Student
#     fields = ['first_name', 'last_name', 'address', 'city', 'date_of_birth', 'date_of_joining', 'phone_number', 'rank',
#               'guardian']

def student_create(request):
    if request.POST:
        stu_form = StudentForm(request.POST or None, prefix="student")
        en_form = EnrollmentForm(request.POST or None)
        guardian_form = GuardianForm(request.POST or None, prefix="guardian")
        if stu_form.is_valid() and en_form.is_valid() and guardian_form.is_valid():
            if guardian_form.has_changed():
                guardian = guardian_form.save()
                student = stu_form.save(commit=False)
                student.guardian = guardian
            student = stu_form.save(commit=False)
            stu_form.save()
            enrollment = en_form.save(commit=False)
            enrollment.student = student
            en_form.save()
            stu = Student.objects.all()
            return render(request, 'student/student.html', {'object_list': stu})
    else:
        stu_form = StudentForm(request.POST or None, prefix="student")
        en_form = EnrollmentForm(request.POST or None)
        guardian_form = GuardianForm(request.POST or None, prefix="guardian")
        return render(request, 'student/student_form.html', {"form": stu_form, "form1": en_form, "form2": guardian_form})

class StudentUpdate(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'street_name', 'city', 'province', 'postal_code', 'date_of_birth', 'date_of_joining', 'phone_number', 'rank',]

class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('student:student')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def student_search(request):
    template = 'student/student.html'

    query = request.GET.get('q')

    results = Student.objects.filter(Q(pk__icontains=query) |
                                     Q(first_name__icontains=query) |
                                     Q(last_name__icontains=query) |
                                     Q(guardian__first_name__icontains=query) |
                                     Q(guardian__last_name__icontains=query))

    context = {
        'object_list': results
    }

    return render(request, template, context)

# Enrollments
class EnrollIndexView(generic.ListView):
    template_name = 'student/enroll.html'

    def get_queryset(self):
        return Enrollment.objects.all()

class EnrollCreate(CreateView):
    model = Enrollment
    fields = ['student', 'batch']

class EnrollUpdate(UpdateView):
    model = Enrollment
    fields = ['student', 'batch']

class EnrollDelete(DeleteView):
    model = Enrollment
    success_url = reverse_lazy('student:enroll')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def enroll_search(request):
    template = 'student/enroll.html'

    query = request.GET.get('q')

    results = Enrollment.objects.filter(Q(batch__batch_day__icontains=query) |
                                        Q(student__first_name__icontains=query) |
                                        Q(student__last_name__icontains=query) |
                                        Q(batch__level__level_name__icontains=query))

    context = {
        'object_list': results
    }

    return render(request, template, context)

def guardian_create(request, pk):
    if request.POST:
        guardian_form = GuardianForm(request.POST or None, prefix="guardian")
        student = Student.objects.get(pk=pk)
        if guardian_form.is_valid():
            guardian = guardian_form.save()
            student.guardian = guardian
            student.save(force_update=True)
            stu = Student.objects.get(pk=pk)
            return render(request, 'student/student.html', {"object_list": stu})
    else:
        guardian_form = GuardianForm(request.POST or None, prefix="guardian")
        return render(request, 'student/student_form.html', {"form": guardian_form})

def progress_add(request, pk):
    if request.POST:
        progress_form = ProgressForm(request.POST or None, prefix="progress")
        student = Student.objects.get(pk=pk)
        if progress_form.is_valid():
            progress = progress_form.save(commit=False)
            progress.student = student
            student.rank = progress.progress_belt_to
            progress.save()
            student.save(force_update=True)
            stu = Student.objects.all()
            return render(request, 'student/student.html', {"object_list": stu})
            #return reverse('student:detail', args=[pk])
    else:
        progress_form = ProgressForm(request.POST or None, prefix="progress")
        return render(request, 'student/progress_form.html', {"form": progress_form})


class GuardianCreate(CreateView):
    model = Guardian
    fields = ['first_name', 'last_name', 'street_name', 'city', 'province', 'postal_code', 'phone_number', 'relation']

#Batch Information Pages
class BatchIndexView(generic.ListView):
    template_name = 'student/batch.html'

    def get_queryset(self):
        return Batch.objects.all()

class BatchCreate(CreateView):
    model = Batch
    fields = ['batch_day', 'batch_start_time', 'batch_end_time', 'level', 'instructor']

class BatchUpdate(UpdateView):
    model = Batch
    fields = ['batch_day', 'batch_start_time', 'batch_end_time', 'level', 'instructor']

class BatchDelete(DeleteView):
    model = Batch
    success_url = reverse_lazy('student:batch')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# Students in given Batch
def batchstudent(request, pk):
    enrolls = Enrollment.objects.filter(batch=pk)
    students = []
    for enroll in enrolls:
        students.append(enroll.student)
    return render(request, 'student/student.html', { 'object_list': students })

# Attendance Page
class AttendanceIndexView(generic.ListView):
    template_name = 'student/attend.html'

    def get_queryset(self):
        return Attendance.objects.all()

class AttendanceCreate(CreateView):
    model = Attendance
    fields = ['student', 'attendance_date', 'attendance_count']

class AttendanceUpdate(UpdateView):
    model = Attendance
    fields = ['student', 'attendance_date', 'attendance_count']

class AttendanceDelete(DeleteView):
    model = Attendance
    success_url = reverse_lazy('student:attend')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def attendance_search(request):
    template = 'student/attend.html'

    query = request.GET.get('q')

    results = Attendance.objects.filter(Q(attendance_date__icontains=query) |
                                        Q(student__first_name__icontains=query) |
                                        Q(student__last_name__icontains=query))

    context = {
        'object_list': results
    }

    return render(request, template, context)

# Finance Page
class FinanceIndexView(generic.ListView):
    template_name = 'student/finance.html'

    def get_queryset(self):
        return Fee.objects.all()

class FinanceCreate(CreateView):
    model = Fee
    fields = ['fee_name', 'fee_date', 'fee_amount', 'student']

class FinanceUpdate(UpdateView):
    model = Fee
    fields = ['fee_name', 'fee_date', 'fee_amount']

class FinanceDelete(DeleteView):
    model = Fee
    success_url = reverse_lazy('student:finance')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def monthly_report(request):

    query = """SELECT 1 as id,  
                CASE strftime('%m',fee_date) WHEN '01' then 'January' 
                                            when '02' then 'Febuary' 
                                            when '03' then 'March' 
                                            when '04' then 'April' 
                                            when '05' then 'May' 
                                            when '06' then 'June' 
                                            when '07' then 'July' 
                                            when '08' then 'August' 
                                            when '09' then 'September' 
                                            when '10' then 'October' 
                                            when '11' then 'November' 
                                            when '12' then 'December' END AS month,
                SUM(fee_amount) as amount 
                FROM student_fee 
                GROUP BY month"""

    fee = Fee.objects.raw(query)

    return render(request, 'student/report.html', {'report': fee})

def finance_search(request):
    template = 'student/finance.html'

    query = request.GET.get('q')

    results = Fee.objects.filter(Q(fee_name__icontains=query) |
                                Q(fee_date__icontains=query) |
                                Q(fee_amount__icontains=query) |
                                Q(student__first_name__icontains=query) |
                                Q(student__last_name__icontains=query))

    context = {
        'object_list': results
    }

    return render(request, template, context)

