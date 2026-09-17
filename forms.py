# admission/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile, AdmissionApplication
import datetime


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['phone', 'date_of_birth', 'gender', 'address', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_profile_picture(self):
        """✅ Handle any image type without errors"""
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp']
            if hasattr(picture, 'content_type'):
                if picture.content_type not in allowed_types:
                    raise forms.ValidationError("Please upload a valid image (JPG, PNG, GIF, WEBP).")
            # Max 5MB
            if hasattr(picture, 'size') and picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image size must be under 5MB.")
        return picture


class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        exclude = ['student', 'application_number', 'status', 'applied_on', 'remarks']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_twelfth_percentage(self):
        pct = self.cleaned_data.get('twelfth_percentage')
        if pct and (pct < 0 or pct > 100):
            raise forms.ValidationError("Percentage must be between 0 and 100.")
        return pct