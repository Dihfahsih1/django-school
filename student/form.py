from django import forms
from django.contrib.auth.models import User

from .models import Student, Guardian, Enrollment, Progress, Batch

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'street_name', 'city', 'province', 'postal_code', 'date_of_birth',
                  'date_of_joining', 'phone_number', 'rank']
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        }

class GuardianForm(forms.ModelForm):

    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    street_name = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    province = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=10, required=False)
    phone_number = forms.CharField(max_length=17, required=False)
    relation = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Guardian
        fields = ['first_name', 'last_name', 'street_name', 'city', 'province', 'postal_code', 'phone_number', 'relation']

class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = Enrollment
        fields = ['batch']

class ProgressForm(forms.ModelForm):

    class Meta:
        model = Progress
        fields = ['progress_belt_from', 'progress_belt_to', 'progress_date']

class BatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BatchForm, self).__init__(*args, **kwargs)
        self.fields['batch_start_time'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['batch_end_time'].widget.attrs['placeholder'] = 'HH:MM'
