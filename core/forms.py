from django import forms
from django.forms import modelformset_factory
from .models import Attendance, Student

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'is_present']
        widgets = {
            'student': forms.HiddenInput(), # Hide the student ID (we know who they are)
            'is_present': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

# Create a FormSet: This allows us to edit multiple Attendance records at once
AttendanceFormSet = modelformset_factory(Attendance, form=AttendanceForm, extra=0)