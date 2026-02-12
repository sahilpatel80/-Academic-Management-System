# school_admin/urls.py

from django.urls import path, include
from . import views

app_name = 'school_admin'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('', include('core.urls')),
    # path('staff/', include('staff.urls')),
    # path('admin-panel/', include('school_admin.urls')),
]
