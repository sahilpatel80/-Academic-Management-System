import calendar
from core.models import Student, Attendance  # Ensure imports are correct
from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# IMPORT NOTE: Agar models 'core' app me hain to aise import karo:
from core.models import Student, Result, Attendance, Semester, Subject


@login_required(login_url="login")
def student_dashboard(request):
    try:
        student_profile = request.user.student
    except AttributeError:
        return render(request, "error.html", {"message": "Student profile not found."})

    results = Result.objects.filter(student=student_profile)

    # Attendance Logic
    total_days = Attendance.objects.filter(student=student_profile).count()
    present_days = Attendance.objects.filter(
        student=student_profile, is_present=True).count()

    attendance_percentage = ((present_days / total_days)
                             * 100) if total_days > 0 else 0

    context = {
        "student": student_profile,
        "results": results,
        "attendance_percentage": round(attendance_percentage, 2),
    }
    return render(request, "student/dashboard.html", context)


@login_required(login_url="core:login")
def profile(request):
    try:
        student = request.user.student
    except AttributeError:
        return render(request, "error.html", {"message": "Not a student"})

    total_day = Attendance.objects.filter(student=student).count()
    present_day = Attendance.objects.filter(
        student=student, is_present=True).count()
    attendance_percentage = round(
        (present_day / total_day) * 100) if total_day > 0 else 0

    dash_offset = 100 - attendance_percentage

    results = Result.objects.filter(student=student)
    performance = [r.total_marks for r in results]

    context = {
        "performance": performance,
        "student": student,
        "attendance_percentage": attendance_percentage,
        "present_day": present_day,
        "total_days": total_day,
        "dash_offset": round(dash_offset, 2),

    }
    return render(request, "student/profile.html", context)


@login_required(login_url="login")
def exam_results(request):
    student = request.user.student
    results = Result.objects.filter(student=student)
    return render(request, "student/results.html", {"student": student, "results": results})


@login_required(login_url="login")
def syllabus(request):
    semesters = Semester.objects.all()
    selected_semester = request.GET.get("semester")

    if selected_semester:
        # Ab hum 'Subject' table filter kar rahe hain kyunki syllabus wahi hai
        subjects = Subject.objects.filter(semester__id=selected_semester)
    else:
        subjects = Subject.objects.all()

    context = {
        # Variable rename kiya (syllabus_list -> subjects)
        "subjects": subjects,
        "semesters": semesters,
        "selected_semester": int(selected_semester) if selected_semester else None,
    }
    return render(request, "student/syllabus.html", context)

# Simple Views (Student folder me move kar diya)


@login_required(login_url="login")
def academics(request): return render(request, "student/academics.html")


@login_required(login_url="login")
def assignments(request): return render(request, "student/assignments.html")


@login_required(login_url="login")
def fees(request): return render(request, "student/fees.html")


@login_required(login_url="login")
def classes(request): return render(request, "student/classes.html")


@login_required(login_url="login")
def calendar_view(request): return render(request, "student/calendar.html")


@login_required(login_url="login")
def chat(request): return render(request, "student/chat.html")


@login_required(login_url="login")
def settings(request): return render(request, "student/settings.html")


@login_required(login_url="core:login")
def attendance(request):
    student = request.user.student

    # 1. Get Year and Month from URL (e.g., ?year=2026&month=3)
    # Default to current date if not provided
    today = datetime.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # 2. Calculate Next/Previous Month links
    # Logic to handle December -> January transition
    prev_date = date(year, month, 1) - timedelta(days=1)
    next_date = date(year, month, 28) + \
        timedelta(days=5)  # Go to next month safely

    prev_month_url = f"?year={prev_date.year}&month={prev_date.month}"
    next_month_url = f"?year={next_date.year}&month={next_date.month}"

    current_month_name = date(year, month, 1).strftime('%B %Y')

    # 3. Generate the Calendar Grid
    cal = calendar.Calendar(firstweekday=5)
    # Returns matrix [[0,0,1,2..], [..]]
    month_days = cal.monthdayscalendar(year, month)

    # 4. Fetch Attendance Data for this specific month
    attendance_records = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month
    )

    # Create a quick lookup dictionary: { day_number: 'Present/Absent' }
    status_map = {}
    for record in attendance_records:
        # Assuming you have a field 'is_present' (Boolean)
        status_map[record.date.day] = 'present' if record.is_present else 'absent'

    # 5. Flatten the matrix and add status
    calendar_data = []
    for week in month_days:
        for day in week:
            if day == 0:
                calendar_data.append({'day': 0, 'status': 'empty'})
            else:
                # Check our database lookup
                # Default to 'no_class' if no record
                status = status_map.get(day, 'no_class')
                calendar_data.append({'day': day, 'status': status})

    # --- (Keep your existing Overall Percentage logic here) ---

    context = {
        "calendar_data": calendar_data,     # List of days with status
        "current_month": current_month_name,
        "prev_link": prev_month_url,
        "next_link": next_month_url,
        "student": student,
        # Add your other stats context here...
    }

    return render(request, "student/attendance.html", context)
