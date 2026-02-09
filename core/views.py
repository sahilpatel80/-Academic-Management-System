# from .models import Semester, Syllabus
# from django.shortcuts import render
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Student, Result, Attendance


# @login_required(login_url='login')
# def student_dashboard(request):
#     try:
#         # 2. Get the Student profile linked to the currently logged-in User
#         student_profile = request.user.student
#     except Student.DoesNotExist:
#         # If the user is an Admin or Staff without a student profile
#         return render(request, 'error.html', {'message': "You are not registered as a Student."})
#     results = Result.objects.filter(student=student_profile)

#     # Calculate Attendance Percentage
#     total_days = Attendance.objects.filter(student=student_profile).count()
#     present_days = Attendance.objects.filter(
#         student=student_profile, is_present=True).count()

#     if total_days > 0:
#         attendance_percentage = (present_days / total_days) * 100
#     else:
#         attendance_percentage = 0

#     context = {
#         'student': student_profile,
#         'results': results,
#         'attendance_percentage': round(attendance_percentage, 2)
#     }
#     return render(request, 'dashboard.html', context)


# def academics(request):
#     return render(request, 'academics.html')


# def assignments(request):
#     return render(request, 'assignments.html')


# def fees(request):
#     return render(request, 'fees.html')


# def profile(request):
#     return render(request, 'profile.html')


# def chat(request):
#     return render(request, 'cht.html')


# def settings(request):
#     return render(request, 'settings.html')


# def classes(request):
#     return render(request, 'classes.html')


# def calendar(request):
#     return render(request, 'calendar.html')


# def syllabus(request):
#     semesters = Semester.objects.all()
#     selected_semester = request.GET.get('semester')

#     if selected_semester:
#         syllabus_list = Syllabus.objects.filter(semester__id=selected_semester)
#     else:
#         syllabus_list = Syllabus.objects.all()

#     context = {
#         'syllabus_list': syllabus_list,
#         'semesters': semesters,
#         'selected_semester': selected_semester,
#     }
#     return render(request, 'syllabus/courses.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    Student,
    Result,
    Attendance,
    Semester,
    Syllabus
)

# =========================
# LOGIN VIEW (STUDENT / STAFF / ADMIN)
# =========================


def user_login(request):
    if request.method == "POST":
        role = request.POST.get("role")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        # =========================
        # STUDENT
        # =========================
        if role == "student":
            if not hasattr(user, "student"):
                messages.error(request, "Student account not found")
                return redirect("login")

            login(request, user)
            return redirect("student_dashboard")

        # =========================
        # STAFF
        # =========================
        elif role == "staff":
            if not hasattr(user, "staff"):
                messages.error(request, "Staff account not found")
                return redirect("login")

            login(request, user)
            return redirect("staff_dashboard")

        # =========================
        # ADMIN
        # =========================
        elif role == "admin":
            if not hasattr(user, "admin_profile"):
                messages.error(request, "Admin account not found")
                return redirect("login")

            login(request, user)
            return redirect("admin_dashboard")

        else:
            messages.error(request, "Invalid role selected")
            return redirect("login")

    return render(request, "login.html")

# =========================
# STUDENT DASHBOARD
# =========================


@login_required(login_url="login")
def student_dashboard(request):
    try:
        student_profile = request.user.student
    except Student.DoesNotExist:
        return render(
            request,
            "error.html",
            {"message": "You are not registered as a Student."}
        )

    results = Result.objects.filter(student=student_profile)

    total_days = Attendance.objects.filter(student=student_profile).count()
    present_days = Attendance.objects.filter(
        student=student_profile,
        is_present=True
    ).count()

    attendance_percentage = (
        (present_days / total_days) * 100 if total_days > 0 else 0
    )

    context = {
        "student": student_profile,
        "results": results,
        "attendance_percentage": round(attendance_percentage, 2),
    }

    return render(request, "dashboard.html", context)


# =========================
# STAFF DASHBOARD
# =========================
@login_required(login_url="login")
def staff_dashboard(request):
    if not hasattr(request.user, "staff"):
        return render(request, "error.html", {
            "message": "Staff access only"
        })

    return render(request, "staff_dashboard.html")


# =========================
# ADMIN DASHBOARD
# =========================
@login_required(login_url="login")
def admin_dashboard(request):
    if not hasattr(request.user, "admin_profile"):
        return render(request, "error.html", {
            "message": "Admin access only"
        })

    return render(request, "admin_dashboard.html")


# =========================
# SIMPLE PAGES
# =========================
@login_required(login_url="login")
def academics(request):
    return render(request, "academics.html")


@login_required(login_url="login")
def assignments(request):
    return render(request, "assignments.html")


@login_required(login_url="login")
def fees(request):
    return render(request, "fees.html")


@login_required(login_url="login")
def profile(request):
    performance = [70, 85, 95, 80, 90]

    context = {
        "performance": performance
    }
    return render(request, "profile.html", context)


@login_required(login_url="login")
def chat(request):
    return render(request, "chat.html")


@login_required(login_url="login")
def settings(request):
    return render(request, "settings.html")


@login_required(login_url="login")
def classes(request):
    return render(request, "classes.html")


@login_required(login_url="login")
def calendar(request):
    return render(request, "calendar.html")


# =========================
# SYLLABUS
# =========================
@login_required(login_url="login")
def syllabus(request):
    semesters = Semester.objects.all()
    selected_semester = request.GET.get("semester")

    if selected_semester:
        syllabus_list = Syllabus.objects.filter(
            semester__id=selected_semester
        )
    else:
        syllabus_list = Syllabus.objects.all()

    context = {
        "syllabus_list": syllabus_list,
        "semesters": semesters,
        "selected_semester": selected_semester,
    }

    return render(request, "syllabus/courses.html", context)
