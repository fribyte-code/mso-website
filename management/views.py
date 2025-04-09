from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



@login_required(redirect_field_name="my_redirect_field")
def index(request):
    return HttpResponse("Hello, world. You're at the management index.")

