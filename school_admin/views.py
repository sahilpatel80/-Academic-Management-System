
# (views.py)school_admin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# @login_required(login_url="core:login")
# def admin_dashboard(request):
#     # Check related_name 'admin_profile' or just user.is_superuser
#     if not hasattr(request.user, "admin_profile"):
#         return render(request, "school_admin/error.html", {"message": "Admin access only"})

#     return render(request, "school_admin/dashboard.html")




@login_required(login_url="core:login")
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Admin access only")
        return redirect("core:login")

    return render(request, "school_admin/dashboard.html")
