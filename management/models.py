from django.db import models
from django.contrib.auth.models import User
from wagtail.contrib.forms.models import FormSubmission

# Create your models here.

class Profile(models.Model):

    GENDER_CHOICES = [
        ('M', 'Mann'),
        ('K', 'Kvinne'),
        ('A', 'Annet'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile"
    )
    telefon =  models.TextField(blank=True, null=True)
    kjønn = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    kull = models.TextField(blank=True, null=True)
    erfaren = models.BooleanField(default=False)
    pu_erfaren = models.BooleanField(default=False)
    fus_erfaren = models.BooleanField(default=False)
    timer = models.IntegerField(default=0)
    internundervisning = models.BooleanField(default=False)
    styremedlem = models.BooleanField(default=False)


class Job(models.Model):
    submission = models.OneToOneField(
        FormSubmission,
        on_delete=models.CASCADE,
        related_name="job"
    )

    assigned_to_M = models.ManyToManyField(
        Profile,
        related_name = "assigned_to_M",
        default=None
    )

    assigned_to_F = models.ManyToManyField(
        Profile,
        related_name = "assigned_to_F",
        default=None
    )

    job_is_active = models.BooleanField(default=False)

