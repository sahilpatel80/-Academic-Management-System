from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, StaffSignupForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login


@login_required(login_url="login")
def staff_dashboard(request):
    if not hasattr(request.user, "staff"):
        return render(request, "error.html", {"message": "Staff access only"})

    return render(request, "staff/dashboard.html")


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

            # 3. Auto Login
            login(request, user)

            messages.success(request, "Staff Account Created Successfully!")
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
