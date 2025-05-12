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
from datetime import datetime, timedelta

@login_required(redirect_field_name="next", login_url="/management/login/")
def index(request):

    if request.method == "POST":
        
        #gets a list of all checklisted items and makes a list of them
        selected_jobs = request.POST.getlist('selected_jobs')

        profile = get_object_or_404(Profile, user=request.user)

        jobs = Job.objects.filter(id__in=selected_jobs)

        action = request.POST.get("action")

        if action == "assign":

            if profile.kjønn == "K":
                successful = Job.objects.filter(id__in=selected_jobs, assigned_to_F__isnull=True).update(assigned_to_F=profile)
                if successful:
                    messages.success(request, f"Job(s) successfully assigned to you")
                else:
                    messages.warning(request, f"One or more job is already occupied")
                return redirect('index')

            if profile.kjønn == "M":
                successful = Job.objects.filter(id__in=selected_jobs, assigned_to_M__isnull=True).update(assigned_to_M=profile)
                if successful:
                    messages.success(request, f"Job(s) successfully assigned to you")
                else:
                    messages.warning(request, f"One or more job is already occupied")
                return redirect('index')
        
        elif action == "unassign":
            
            if profile.kjønn == "K":
                successful = Job.objects.filter(id__in=selected_jobs, assigned_to_F=profile).update(assigned_to_F=None)
                if successful:
                    messages.success(request, f"Job(s) successfully unassigned from you")
                else:
                    messages.warning(request, f"Unsuccessful unassign")
                return redirect('index')

            if profile.kjønn == "M":
                successful = Job.objects.filter(id__in=selected_jobs, assigned_to_M=profile).update(assigned_to_M=None)
                if successful:
                    messages.success(request, f"Job(s) successfully unassigned from you")
                else:
                    messages.warning(request, f"Unsuccessful unassign")
                return redirect('index')

        
    jobs = Job.objects.select_related("submission").filter(job_is_active=True).order_by("-submission__submit_time")
    return render(request, "management.html", {
        "jobs": jobs,
    })

def time_to_num(time_str):
    time = time_str.split(':')
    hour = int(time[0])
    minutes = int(time[1])/60
    returnTime = hour + minutes
    return returnTime

@login_required(redirect_field_name="next", login_url="/management/login/")
def my_assigned_jobs(request):

    profile = get_object_or_404(Profile, user=request.user)

    if profile.kjønn == "K":
        my_assigned_jobs = Job.objects.select_related("submission").filter(assigned_to_F=profile).order_by("-submission__submit_time")
        
    else:
        my_assigned_jobs = Job.objects.select_related("submission").filter(assigned_to_M=profile).order_by("-submission__submit_time")

    job_is_completed = Job.objects.select_related("submission").filter(job_is_completed=True).order_by("-submission__submit_time")

    if request.method == "POST":

        #gets a list of all checklisted items and makes a list of them
        selected_jobs = request.POST.getlist('selected_jobs')

        jobs = Job.objects.filter(id__in=selected_jobs)

        action = request.POST.get("action")

        if action == "job_is_completed":
            Job.objects.filter(id__in=selected_jobs).update(
            job_is_completed=Case(
                When(job_is_completed=False, then=Value(True)),
                default=Value(False))
            )
    
            user_work_time = profile.timer

            for each_job in jobs:
                start_time = each_job.submission.form_data['start_tid']
                end_time = each_job.submission.form_data['slutt_tid']

                start_dt = datetime.strptime(start_time, "%H:%M")
                end_dt = datetime.strptime(end_time, "%H:%M")

                job_duration = end_dt - start_dt

                int_job_duration = time_to_num(str(job_duration))

                if not each_job.job_is_completed:
                    user_work_time -= int_job_duration
                else:
                    user_work_time += int_job_duration

            print(user_work_time)

    
        profile.timer = user_work_time
        profile.save(update_fields=["timer"])                 

    return render(request, "management/my_assigned_jobs.html", {
            "my_assigned_jobs": my_assigned_jobs,
            "job_is_completed": job_is_completed,
        })
   
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

    job_is_completed = Job.objects.select_related("submission").filter(job_is_completed=True).order_by("-submission__submit_time")

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
        "job_is_completed": job_is_completed,
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





