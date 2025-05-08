from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from wagtail.contrib.forms.models import FormSubmission
from home.models import FormPage


@login_required(redirect_field_name="next", login_url="/management/login/")
def index(request):
    return render(request, "management.html")

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required(redirect_field_name="next", login_url="/management/login/")
def profile(request):
    return render(request, "management/profile.html", {
        "user": request.user,
    })

@login_required(redirect_field_name="next", login_url="/management/login/")
def jobs(request):

    form_submissions = FormSubmission.objects.filter(page__in=FormPage.objects.all()).order_by('-submit_time')

    return render(request, "management/jobs.html", {
        "form_submissions": form_submissions
    })

