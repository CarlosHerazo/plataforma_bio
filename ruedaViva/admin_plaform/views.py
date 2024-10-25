from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UsuarioForm
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


def es_admin(user):
    return user.is_superuser # validacion para administrador


@user_passes_test(es_admin)
def index_admin(request):
    return render(request,"admin/index.html")  


@user_passes_test(es_admin)
def usuarios(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario agregado exitosamente!')
            return redirect('usuarios_admin')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = UsuarioForm()

    usuarios = User.objects.all()
    context = {'usuarios': usuarios, 'form': form}
    return render(request, 'admin/usuarios.html', context)

def maps_views(request):
    return render(request, 'admin/maps-google.html')