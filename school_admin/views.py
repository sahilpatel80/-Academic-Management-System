from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="core:login")
def admin_dashboard(request):
    # Check related_name 'admin_profile' or just user.is_superuser
    if not hasattr(request.user, "admin_profile"):
        return render(request, "school_admin/error.html", {"message": "Admin access only"})

    return render(request, "school_admin/dashboard.html")
