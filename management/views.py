from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import Profile, Job
from .forms import ProfileForm, AdminProfileForm, CreateUser
from django.contrib.auth.models import User, Group
from django.contrib import messages 
from django.db.models import Case, When, Value
from datetime import datetime

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

def days_to_months(days, avg_days_per_month=30.44):
    return days / avg_days_per_month

def get_most_recent_job_date(job):
    job_date = job.submission.form_data['dato']
    today = datetime.today().strftime("%Y-%m-%d")

    d1 = datetime.strptime(job_date, "%Y-%m-%d")
    d2 = datetime.strptime(today, "%Y-%m-%d")

    delta_days = abs((d2 - d1).days)
    months = int(days_to_months(delta_days))
    
    return (months, job_date)

@login_required(redirect_field_name="next", login_url="/management/login/")
def my_assigned_jobs(request):

    profile = get_object_or_404(Profile, user=request.user)
    months_since_last_job = profile.months_since_last_job
    last_job_date = profile.last_job_date

    #Toggle job assignment

    if profile.kjønn == "K":
        my_assigned_jobs = Job.objects.select_related("submission").filter(assigned_to_F=profile).order_by("-submission__submit_time")
        
    else:
        my_assigned_jobs = Job.objects.select_related("submission").filter(assigned_to_M=profile).order_by("-submission__submit_time")

    job_is_completed = Job.objects.select_related("submission").filter(job_is_completed=True).order_by("-submission__submit_time")

    if request.method == "POST":

        selected_jobs = request.POST.getlist('selected_jobs')

        jobs = Job.objects.filter(id__in=selected_jobs)

        action = request.POST.get("action")

        if action == "job_is_completed":
            Job.objects.filter(id__in=selected_jobs).update(
            job_is_completed=Case(
                When(job_is_completed=False, then=Value(True)),
                default=Value(False))
            )

            #Calculate duration of job and adjust user_work_time field in model    
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

                    

            #Find most recent job

            for each_job in jobs:
                deltaDates = get_most_recent_job_date(each_job)
                months = deltaDates[0]
                if months_since_last_job is None: 
                    months_since_last_job = deltaDates[0]
                    last_job_date = deltaDates[1]
                if months >= months_since_last_job:
                    months_since_last_job = deltaDates[0]
                    last_job_date = deltaDates[1]

                if not each_job.job_is_completed:
                    months_since_last_job = None 
                    last_job_date = None


        profile.timer = user_work_time
        profile.months_since_last_job = months_since_last_job
        profile.last_job_date = last_job_date
        profile.save(update_fields=["timer", "months_since_last_job", "last_job_date"])  


    return render(request, "management/my_assigned_jobs.html", {
            "my_assigned_jobs": my_assigned_jobs,
            "job_is_completed": job_is_completed,
            "months_since_last_job": months_since_last_job,
            "last_job_date": last_job_date,
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
    user: User = get_object_or_404(User, pk=pk)
    profile, created = Profile.objects.get_or_create(user=user)

    form = AdminProfileForm(request.POST or None,
                            request.FILES or None,
                            instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()

        # Flipping is_staff gives access to more advanced views
        # adding group gives access to edit the pages in wagtail admin
        grp = Group.objects.get(name="Moderators")
        if form.cleaned_data["styremedlem"]:
            user.is_staff = True
            user.groups.add(grp)
        else:
            user.is_staff = False
            user.groups.remove(grp)

        user.save()

        return redirect('/management/admin', pk=pk)

    return render(request, 'management/admin/profile_edit.html', {
        'form':   form,
        'user':   user,
        'profile': profile,
    })

@staff_member_required(redirect_field_name="next", login_url="/management/login/")
def create_new_user(request):

    form = CreateUser(request.POST or None,
                                request.FILES or None)

    if request.method == 'POST':
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, password=password)

        user.save()

        return redirect(f"/management/admin/profile_edit/{user.id}/")

    return render(request, 'management/admin/create_new_user.html', {
        'form':   form,
    })



