# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('core.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# school_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views
# urlpatterns = [
#     # Django ka default Admin Panel
#     path('admin/', admin.site.urls),

#     # 1. CORE APP (Login, Logout, Home) - Root URL ('')
#     path('', include('core.urls')),

#     # 2. STUDENT APP (Saare student pages yahan)
#     path('student/', include('student.urls')),

#     # 3. STAFF APP
#     path('staff/', include('staff.urls')),

#     # 4. SCHOOL ADMIN (Custom Dashboard)
#     # Iska naam maine 'manager' rakha hai taaki default 'admin' se conflict na ho
#     path('manager/', include('school_admin.urls')),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('student/', include('student.urls')),
    path('staff/', include('staff.urls')),
    path('school-admin/', include('school_admin.urls')),


    path('', core_views.home, name='root_home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
