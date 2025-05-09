from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ["telefon", "kjønn", "kull", "erfaren", "pu_erfaren", "fus_erfaren", "over_72h", "internundervisning", "styremedlem"]
        