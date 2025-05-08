from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout


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
    return render(request, "management/jobs.html")