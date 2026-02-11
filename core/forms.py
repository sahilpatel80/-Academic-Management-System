# student/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Student

# 1. Login Details Form (Username, Password)


class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# 2. Student Details Form (Roll No, Class, etc.)


class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'roll_no',
            'student_class',
            'dob',
            'enrollment_no',
            'department',
            'phone_number',
            'profile_pic'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
