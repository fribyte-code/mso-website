from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(redirect_field_name="my_redirect_field", login_url="/admin/login/")
def index(request):
    return render(request, "management.html")

