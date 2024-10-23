from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


def es_admin(user):
    return user.is_superuser # validacion para administrador


@user_passes_test(es_admin)
def index_admin(request):
    return render(request,"admin/index.html")  
