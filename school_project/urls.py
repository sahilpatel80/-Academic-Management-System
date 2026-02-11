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

urlpatterns = [
    # Django ka default Admin Panel
    path('admin/', admin.site.urls),

    # 1. CORE APP (Login, Logout, Home) - Root URL ('')
    path('', include('core.urls')),

    # 2. STUDENT APP (Saare student pages yahan)
    path('student/', include('student.urls')),

    # 3. STAFF APP
    path('staff/', include('staff.urls')),

    # 4. SCHOOL ADMIN (Custom Dashboard)
    # Iska naam maine 'manager' rakha hai taaki default 'admin' se conflict na ho
    path('manager/', include('school_admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
