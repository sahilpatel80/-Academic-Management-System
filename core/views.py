from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Student, ClassName
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, StudentSignupForm


def student_signup(request):
    classes = ClassName.objects.all()

    if request.method == "POST":
        user_form = UserSignupForm(request.POST)
        student_form = StudentSignupForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            student = student_form.save(commit=False)
            student.user = user
            student.save()

            messages.success(
                request, "Account created successfully. Please login.")
            return redirect('core:login')
        else:
            messages.error(request, "Form error. Please check details.")

    else:
        user_form = UserSignupForm()
        student_form = StudentSignupForm()

    return render(request, 'core/signup.html', {
        'user_form': user_form,
        'student_form': student_form,
        'classes': classes
    })


# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user:
#             login(request, user)
#             return redirect('student_dashboard')  # ✅ FIXED
#         else:
#             messages.error(request, "Invalid username or password")
#             return redirect('login')

#     return render(request, 'core/login.html')

def user_login(request):
    # 1. If the user is already authenticated, redirect them to their respective dashboard
    if request.user.is_authenticated:
        if hasattr(request.user, 'student'):
            return redirect('student:student_dashboard')
        elif hasattr(request.user, 'staff'):
            return redirect('staff:staff_dashboard')
        elif request.user.is_superuser:
            return redirect('admin_dashboard')

    # 2. Handle Form Submission
    if request.method == "POST":
        # Retrieve the role (student/staff/admin) from HTML
        role = request.POST.get("role")
        username = request.POST.get("username")
        password = request.POST.get("password")
        enrollment_no = request.POST.get('enrollment_no')

        user = authenticate(request, username=username,
                            password=password, enrollment_no=enrollment_no)

        if user is not None:
            # --- START STRICT ROLE ENFORCEMENT ---

            # CASE 1: User selected STUDENT
            if role == 'student':
                if hasattr(user, 'student'):  # Check: Does a Student profile exist for this user?
                    login(request, user)
                    return redirect('student:student_dashboard')
                else:
                    # Credentials are correct, but the user is not a Student
                    messages.error(
                        request, "Access Denied: This account is not registered as a Student.")

            # CASE 2: User selected STAFF
            elif role == 'staff':
                if hasattr(user, 'staff'):    # Check: Does a Staff profile exist for this user?
                    login(request, user)
                    return redirect('staff_dashboard')
                else:
                    messages.error(
                        request, "Access Denied: This account is not registered as Staff.")

            # CASE 3: User selected ADMIN
            elif role == 'admin':
                if user.is_superuser:         # Check: Is the user a Superuser?
                    login(request, user)
                    return redirect('admin_dashboard')
                else:
                    messages.error(
                        request, "Access Denied: You do not have Administrator privileges.")

            # Fallback if no valid role was selected
            else:
                messages.error(request, "Please select a valid role.")

        else:
            # Authentication failed (Invalid Username or Password)
            messages.error(request, "Invalid Username or Password.")

    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect('core:login')


@login_required(login_url='core:login')
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect('core:login')

    return render(request, 'student/dashboard.html', {'student': student})


# def signup_router(request):
#     role = request.GET.get('role')

#     if role == 'student':
#         return redirect('core:signup')
#     elif role == 'staff':
#         return redirect('staff:signup')
#     elif role == 'school_admin':
#         return redirect('school_admin:admin_signup')
#     else:
#         messages.error(request, "Invalid Signup request")
#         return redirect('core:login')

@login_required(login_url='core:login')
def login_redirect(request):
    user = request.user

    if user.is_superuser:
        return redirect('school_admin:admin_dashboard')

    if hasattr(user, 'staff'):
        return redirect('staff:staff_dashboard')

    if hasattr(user, 'student'):
        return redirect('student:student_dashboard')

    messages.error(request, "No role assigned to this account")
    return redirect('core:login')
