# student/urls.py

from django.urls import path
from . import views

app_name = 'student'
urlpatterns = [
    # Dashboard
    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    # Profile & Results
    path('profile/', views.profile, name='profile'),
    path('results/', views.exam_results, name='exam_results'),

    # Academics
    path('academics/', views.academics, name='academics'),
    path('syllabus/', views.syllabus, name='syllabus'),
    path('classes/', views.classes, name='classes'),
    path('assignments/', views.assignments, name='assignments'),

    # Others
    path('attendance/', views.attendance, name='attendance'),
    path('fees/', views.fees, name='fees'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('chat/', views.chat, name='chat'),
    path('settings/', views.settings, name='settings'),

]
