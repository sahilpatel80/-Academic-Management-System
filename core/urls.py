# from django.urls import path
# from . import views
# from django.contrib.auth import views as auth_views
# from django.views.generic import RedirectView

# urlpatterns = [
#     path('', RedirectView.as_view(url='login/')),
#     path('dashboard/', views.student_dashboard, name='student_dashboard'),
#     # path('student/<int:student_id>/', views.student_dashboard, name='student_dashboard'),

#     # login & logout
#     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
#     path('academics/', views.academics, name='academics'),
#     path('assignments/', views.assignments, name='assignments'),
#     path('fees/', views.fees, name='fees'),
#     path('profile/', views.profile, name='profile'),
#     path('classes/', views.classes, name='classes'),
#     path('chat/', views.chat, name='chat'),
#     path('settings/', views.settings, name='settings'),
#     path('calendar/', views.calendar, name='calendar'),
#     path('syllabus/', views.syllabus, name='syllabus'),
#     path('results/', views.exam_results, name='results'),
#     path('attendance',views.attendance, name='attendance'),

# ]
# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.student_signup, name='signup'),
    # path('send-otp/', views.send_otp, name='send_otp'),
    # path('signup-router/', views.signup_router, name='signup_router'),
    # core/urls.py
    path('redirect/', views.login_redirect, name='login_redirect'),

]
