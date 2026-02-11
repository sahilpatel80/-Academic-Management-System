# staff/urls.py

from django.urls import path
from . import views

app_name = 'staff'


urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff_signup/', views.staff_signup, name='staff_signup'),
]
