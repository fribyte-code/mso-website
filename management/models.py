from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    telefon =  models.TextField(blank=True, null=True)
    kjønn = models.TextField(blank=True, null=True)
    kull = models.TextField(blank=True, null=True)
    erfaren = models.BooleanField(default=False)
    pu_erfaren = models.BooleanField(default=False)
    fus_erfaren = models.BooleanField(default=False)
    over_72h = models.BooleanField(default=False)
    internundervisning = models.BooleanField(default=False)
    styremedlem = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name}'s profile"