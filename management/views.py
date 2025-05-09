from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from wagtail.contrib.forms.models import FormSubmission
from home.models import FormPage
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.contrib import messages 

@login_required(redirect_field_name="next", login_url="/management/login/")
def index(request):
    return render(request, "management.html")

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required(redirect_field_name="next", login_url="/management/login/")
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "management/profile.html", {
        "user": request.user,
        "profile": profile
    })

@login_required(redirect_field_name="next", login_url="/management/login/")
def profile_edit(request):
    # ensure a Profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilen din er oppdatert.")
            return redirect("profile.html")   # back to your view-profile URL
    else:
        form = ProfileForm(instance=profile)

    return render(request, "management/profile/edit.html", {
        "form": form,
    })


@login_required(redirect_field_name="next", login_url="/management/login/")
def jobs(request):

    form_submissions = FormSubmission.objects.filter(page__in=FormPage.objects.all()).order_by('-submit_time')

    return render(request, "management/jobs.html", {
        "form_submissions": form_submissions
    })



