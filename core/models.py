from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ==========================================
# 1. ACADEMIC STRUCTURE & Staff(Classes & Semesters & Staff )
# ==========================================


class Staff(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --- 1. Personal Details ---
    name = models.CharField(max_length=100)
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_pic = models.ImageField(
        upload_to='staff_pics/', blank=True, null=True)

    # --- 2. Contact Details ---
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    # --- 3. Professional Details ---
    school_name = models.CharField(
        max_length=200, default="Academic Cloud University")  # <--- NEW FIELD
    department = models.CharField(max_length=100)  # e.g. Science, Admin
    designation = models.CharField(max_length=100)  # e.g. Teacher, HOD
    qualification = models.CharField(max_length=200)  # e.g. M.Sc, B.Ed

    def __str__(self):
        return f"{self.name} - {self.designation}"


class Semester(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Fall 2025", "Semester 1"
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self): return self.name


class ClassName(models.Model):
    # e.g., "Class 10-A", "CS-Final Year"
    name = models.CharField(max_length=50)

    def __str__(self): return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Mathematics"
    course_code = models.CharField(
        max_length=20, unique=True, null=True)  # e.g., "MATH101"
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, null=True, related_name="subjects")
    # Syllabus fields merged here
    syllabus_pdf = models.FileField(upload_to='syllabus/', blank=True)
    progress = models.PositiveIntegerField(
        default=0)  # Syllabus completion % (e.g., 75)

    def __str__(self): return f"{self.name} ({self.class_name})"


class Lecture(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="lectures")

    # Timing Details
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True, null=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    def __str__(self):
        return f"{self.subject.name} - {self.date} ({self.start_time})"

# --- 3. ATTENDANCE SYSTEMS ---

# Teacher ki Attendance (Pure Din ki)


class StaffAttendance(models.Model):
    STATUS_CHOICES = [('Present', 'Present'), ('Absent',
                                               'Absent'), ('Leave', 'On Leave')]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Present')

    class Meta:
        unique_together = ['staff', 'date']  # Ek din mein ek hi attendance

# Student ki Attendance (Lecture ke hisab se)


class StudentAttendance(models.Model):
    STATUS_CHOICES = [('Present', 'Present'),
                      ('Absent', 'Absent'), ('Late', 'Late')]

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Present')
    # Searching ke liye fast rahega
    date = models.DateField(default=timezone.now)

    class Meta:
        # Ek lecture mein duplicate nahi
        unique_together = ['student', 'lecture']

    def __str__(self):
        return f"{self.student.name} - {self.status}"
# ==========================================
# 2. USER PROFILES (Student, Staff, Admin)
# ==========================================


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)

    # Personal Info
    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='students/', blank=True)

    # Academic Info
    roll_no = models.CharField(max_length=20, unique=True)
    enrollment_no = models.CharField(max_length=30, unique=True)
    student_class = models.ForeignKey(
        ClassName, on_delete=models.SET_NULL, null=True, related_name="students")
    department = models.CharField(max_length=100)

    def __str__(self): return f"{self.name} ({self.roll_no})"


class AdminProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="admin_profile")
    role = models.CharField(max_length=50, default="System Administrator")

    def __str__(self): return f"Admin: {self.user.username}"


# ==========================================
# 3. ACADEMIC ACTIVITIES (Assignments & Attendance)
# ==========================================

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    file = models.FileField(upload_to='assignments/',
                            blank=True)  # Teacher uploads Q-paper
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.title


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)

    # Optional: Agar subject-wise attendance chahiye to ise uncomment karein
    # subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        # Ek student ki ek din ki attendance duplicate na ho
        unique_together = ['student', 'date']

    def __str__(self): return f"{self.student.name} - {self.date}"


# ==========================================
# 4. EXAM & RESULT MODELS
# ==========================================

class Exam(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Mid-Term 2026"
    # Exam kis class ke liye hai
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self): return self.name


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(
        max_digits=5, decimal_places=2, default=100.00)

    class Meta:
        unique_together = ['student', 'exam', 'subject']

    def __str__(
        self): return f"{self.student} - {self.subject}: {self.marks_obtained}"


# ==========================================
# 5. FEES MODULE
# ==========================================

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    payment_type = models.CharField(max_length=50, choices=[
        ('Tuition', 'Tuition'),
        ('Bus', 'Bus'),
        ('Exam', 'Exam'),
        ('Hostel', 'Hostel')
    ])
    # Online payment track karne ke liye
    transaction_id = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self): return f"{self.student} - Paid {self.amount_paid}"


# 3. OTP Model (Temporary Storage)
class OTP(models.Model):
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mobile} - {self.otp}"
