from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import DetailsUser
from .forms import UsuarioForm, DetailsUserForm
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
        user_form = UsuarioForm(request.POST)
        details_form = DetailsUserForm(request.POST, request.FILES)  # Asegúrate de manejar archivos

        if user_form.is_valid() and details_form.is_valid():
            user = user_form.save()
            details = details_form.save(commit=False)  # No guardar aún
            details.user = user  # Relacionar con el usuario
            details.save()  # Guardar detalles
            messages.success(request, 'Usuario agregado exitosamente!')
            return redirect('usuarios_admin')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        user_form = UsuarioForm()
        details_form = DetailsUserForm()

    usuarios = DetailsUser.objects.all()
    context = {
        'usuarios': usuarios,
        'user_form': user_form,
        'details_form': details_form,
    }
    
    print(usuarios)
    return render(request, 'admin/usuarios.html', context)

def maps_views(request):
    return render(request, 'admin/maps-google.html')