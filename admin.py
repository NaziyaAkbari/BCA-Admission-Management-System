# admission/admin.py
from django.contrib import admin
from .models import StudentProfile, AdmissionApplication

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'gender']

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'full_name', 'email', 'twelfth_percentage', 'status', 'applied_on']
    list_filter = ['status']
    search_fields = ['full_name', 'application_number', 'email']
    list_editable = ['status']