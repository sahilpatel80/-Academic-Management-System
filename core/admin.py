from django.contrib import admin
from .models import *

admin.site.register(ClassName)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Exam)
admin.site.register(Result)
admin.site.register(FeePayment)
admin.site.register(Attendance)
admin.site.register(Staff)
admin.site.register(AdminProfile)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'subject_name',
                    'semester', 'progress', 'updated_at')
    list_filter = ('semester',)
