from django import forms
from .models import Profile
class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ["telefon", "kjønn", "kull"]

class AdminProfileForm(forms.ModelForm):
    class Meta(ProfileForm.Meta): 
        model = Profile
        fields = ["telefon", "kjønn", "kull", "erfaren", "pu_erfaren", "fus_erfaren", "timer", "internundervisning", "styremedlem", "months_since_last_job"]
