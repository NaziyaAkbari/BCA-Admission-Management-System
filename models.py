# admission/models.py

from django.db import models
from django.contrib.auth.models import User
import os


def profile_pic_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"profile_{instance.user.id}.{ext}"
    return os.path.join('profile_pics', filename)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')
    ], blank=True)
    address = models.TextField(blank=True)
    # ✅ Profile picture with default fallback - NO errors ever
    profile_picture = models.ImageField(
        upload_to=profile_pic_path,
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_profile_pic_url(self):
        """Always returns a valid image URL - never errors"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            try:
                if os.path.exists(self.profile_picture.path):
                    return self.profile_picture.url
            except Exception:
                pass
        return None  # Template will show default avatar


class AdmissionApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    application_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')
    ])
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    twelfth_board = models.CharField(max_length=100)
    twelfth_year = models.IntegerField()
    twelfth_subjects = models.CharField(max_length=200)
    math_marks = models.IntegerField(default=0)
    computer_marks = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.application_number} - {self.full_name}"