from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from wagtail.contrib.forms.models import FormSubmission
from home.models import FormPage
from .models import Profile, Job
from .forms import ProfileForm, AdminProfileForm
from django.contrib.auth.models import User
from django.contrib import messages 
from django.db import models
from django.db.models import Case, When, Value, BooleanField, F

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
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile.html")   # back to your view-profile URL
    else:
        form = ProfileForm(instance=profile)

    return render(request, "management/profile/edit.html", {
        "form": form,
    })


@staff_member_required(redirect_field_name="next", login_url="/management/login/")
def jobs(request):
    if request.method == "POST":
        
        #gets a list of all checklisted items and makes a list of them
        selected_jobs = request.POST.getlist('selected_jobs')

        jobs_to_toggle = Job.objects.filter(id__in=selected_jobs).update(
            job_is_active=Case(
                When(job_is_active=False, then=Value(True)),
                default=Value(False))
            )
        
        return redirect('jobs')  

    jobs = Job.objects.select_related("submission").order_by("-submission__submit_time")
    return render(request, "management/jobs.html", {
        "jobs": jobs,
    })

@staff_member_required(redirect_field_name="next", login_url="/management/login/")
def admin(request):
    users = User.objects.select_related('profile').all()
    
    return render(request, "management/admin.html", {
        'users': users,
    })

@staff_member_required(redirect_field_name="next", login_url="/management/login/")
def admin_profile_edit(request, pk):
    user    = get_object_or_404(User, pk=pk)
    profile, created = Profile.objects.get_or_create(user=user)

    form = AdminProfileForm(request.POST or None,
                            request.FILES or None,
                            instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin-profile-edit', pk=pk)

    return render(request, 'management/admin/profile_edit.html', {
        'form':   form,
        'user':   user,
        'profile': profile,
    })





