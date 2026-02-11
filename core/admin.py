# from django.contrib import admin
# from .models import *

# admin.site.register(ClassName)
# admin.site.register(Student)
# admin.site.register(Subject)
# admin.site.register(Assignment)
# admin.site.register(Exam)
# admin.site.register(Result)
# admin.site.register(FeePayment)
# admin.site.register(Attendance)
# admin.site.register(Staff)
# admin.site.register(AdminProfile)


# @admin.register(Semester)
# class SemesterAdmin(admin.ModelAdmin):
#     list_display = ('name',)


# @admin.register(Syllabus)
# class SyllabusAdmin(admin.ModelAdmin):
#     list_display = ('course_code', 'subject_name',
#                     'semester', 'progress', 'updated_at')
#     list_filter = ('semester',)


from django.contrib import admin
from .models import *

# 1. CLASS & SEMESTER
admin.site.register(ClassName)
admin.site.register(Semester)

# 2. STUDENT (Advanced View)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'student_class',
                    'department')  # Table columns
    # Search bar works on these
    search_fields = ('name', 'roll_no', 'enrollment_no')
    list_filter = ('student_class', 'department')  # Sidebar filters

# 3. STAFF


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'department')
    list_filter = ('department',)

# 4. SUBJECT (Syllabus merged here)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    # Syllabus progress yahan dikhega
    list_display = ('name', 'course_code', 'class_name', 'progress')
    list_filter = ('class_name', 'semester')
    search_fields = ('name', 'course_code')

# 5. ASSIGNMENT


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'deadline')
    list_filter = ('subject',)

# 6. EXAM & RESULT


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'date')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'subject',
                    'marks_obtained', 'total_marks')
    list_filter = ('exam', 'subject')
    # Search by student name
    search_fields = ('student__name', 'student__roll_no')

# 7. FEES


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_paid', 'payment_type', 'date_paid')
    list_filter = ('payment_type', 'date_paid')
    search_fields = ('student__name', 'transaction_id')

# 8. ATTENDANCE


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present')
    # Filter by Class also
    list_filter = ('date', 'is_present', 'student__student_class')


# 9. ADMIN PROFILE
admin.site.register(AdminProfile)
