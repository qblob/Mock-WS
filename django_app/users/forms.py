from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("photo",)
        widgets = {
            "photo": forms.FileInput(),
        }