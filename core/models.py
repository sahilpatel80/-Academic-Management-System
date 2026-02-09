from django.db import models
from django.contrib.auth.models import User

# 1. ACADEMIC MODELS


class ClassName(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Class 10-A"

    def __str__(self): return self.name


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)  # Link to Login
    roll_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    student_class = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    dob = models.DateField()
    enrollment_no = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100)
    profile_pic = models.ImageField(
        upload_to='students/', blank=True)  # For ID Card

    def __str__(self): return f"{self.name} ({self.roll_no})"


class Staff(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff"
    )
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return f"Staff: {self.user.username}"


class AdminProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="admin_profile"
    )
    role = models.CharField(
        max_length=50,
        default="System Administrator"
    )

    def __str__(self):
        return f"Admin: {self.user.username}"


# 2. SYLLABUS & ASSIGNMENT MODELS


class Subject(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Mathematics"
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    syllabus_pdf = models.FileField(
        upload_to='syllabus/', blank=True)  # Syllabus Upload

    def __str__(self): return self.name


class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    file = models.FileField(upload_to='assignments/',
                            blank=True)  # Teacher uploads Q-paper

    def __str__(self): return self.title

# 3. EXAM & RESULT MODELS


class Exam(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Mid-Term 2026"
    date = models.DateField()

    def __str__(self): return self.name


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(
        max_digits=5, decimal_places=2, default=100.00)

    def __str__(
        self): return f"{self.student} - {self.subject}: {self.marks_obtained}"

# 4. FEES MODULE


class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    payment_type = models.CharField(
        max_length=50, choices=[('Tuition', 'Tuition'), ('Bus', 'Bus')])
    remarks = models.TextField(blank=True)

    def __str__(self): return f"{self.student} - Paid {self.amount_paid}"

# 5. ATTENDANCE MODULE


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)

    class Meta:
        unique_together = ['student', 'date']  # Prevent duplicate attendance


class Semester(models.Model):
    name = models.CharField(max_length=50)   # Fall 2024, Spring 2025

    def __str__(self):
        return self.name


class Syllabus(models.Model):
    course_code = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(default=0)  # %
    pdf = models.FileField(upload_to='syllabus_pdfs/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name
