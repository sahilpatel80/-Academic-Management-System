from django import forms
from core.models import Staff
from django.contrib.auth.models import User
from core.forms import UserSignupForm

# 1. Login Details Form (Username, Password)


class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# 2. Student Details Form


class StaffSignupForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'name', 'gender', 'dob', 'profile_pic',
            'phone_number', 'address',
            'school_name',
            'department', 'designation',

        ]

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Full Residential Address'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Years (e.g. 5)'}),
        }
