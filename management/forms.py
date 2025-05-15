from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.forms import CharField

class ProfileForm(forms.ModelForm):
    password = forms.CharField(label="Password", required=False)
    email = forms.CharField(label="Email", required=False)

    class Meta: 
        model = Profile
        fields = ["telefon", "kjønn", "kull"]
        

class AdminProfileForm(forms.ModelForm):

    password = forms.CharField(label="Password", required=False)
    email = forms.CharField(label="Email", required=False)

    class Meta(ProfileForm.Meta): 
        model = Profile
        fields = ["telefon", "kjønn", "kull", "erfaren", "pu_erfaren", "fus_erfaren", "timer", "internundervisning", "styremedlem", "months_since_last_job"]

class CreateUser(forms.ModelForm):
    class Meta(ProfileForm.Meta): 
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

   
