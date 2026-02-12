from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, StaffSignupForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from datetime import date, timedelta
from core.models import Staff, Subject, Student,  StudentAttendance, Lecture
from django.utils import timezone


@login_required(login_url="login")
def staff_dashboard(request):

    if not hasattr(request.user, "staff"):
        return render(request, "error.html", {"message": "Staff access only"})

    staff = request.user.staff

    subjects = Subject.objects.filter(staff=staff)

    tomorrow = date.today() + timedelta(days=1)
    tomorrow_lectures = Lecture.objects.filter(
        subject__staff=staff,
        date=tomorrow
    )

    # 🔥 SAFE DYNAMIC VALUES
    subjects_count = subjects.count()              # auto 0
    # jab tak Student model connect na ho
    students_count = 0
    lecture_hours = Lecture.objects.filter(
        subject__staff=staff
    ).count() or 0                                  # auto 0
    pending_tasks = 0                               # future task model

    context = {
        "staff": staff,
        "subjects_count": subjects_count,
        "students_count": students_count,
        "lecture_hours": lecture_hours,
        "pending_tasks": pending_tasks,
        "tomorrow_lectures": tomorrow_lectures,
        "tomorrow_date": tomorrow,
    }

    return render(request, "staff/dashboard.html", context)


def staff_signup(request):
    if request.method == "POST":
        user_form = UserSignupForm(request.POST)
        staff_form = StaffSignupForm(request.POST, request.FILES)

        if user_form.is_valid() and staff_form.is_valid():
            # 1. User Save
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # 2. Staff Save
            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()

            messages.success(
                request, "Account created successfully. Please login.")
            return redirect('core:login')  # Ensure ye URL exist karta ho

        else:
            messages.error(request, "Error in form details.")

    else:
        user_form = UserSignupForm()
        staff_form = StaffSignupForm()

    return render(request, 'staff/signup.html',  {
        'user_form': user_form,
        'staff_form': staff_form
    })

