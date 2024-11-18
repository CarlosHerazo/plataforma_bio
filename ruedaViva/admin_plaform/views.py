from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import DetailsUser, Container
from .forms import UsuarioForm, DetailsUserForm, ContainerForm, TireDataForm
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

    usuarios = DetailsUser.objects.all()  # Obtener todos los usuarios


    context = {
        'usuarios': usuarios,
        'user_form': user_form,
        'details_form': details_form,
    }
    
    print(usuarios)
    return render(request, 'admin/usuarios.html', context)

@user_passes_test(es_admin)
def editar_usuario(request, id):
    usuario = get_object_or_404(DetailsUser, user__id=id)  # Obtener detalles del usuario por su ID

    if request.method == "POST":
        user_form = UsuarioForm(request.POST, instance=usuario.user)  # Prellenar con datos del usuario
        details_form = DetailsUserForm(request.POST, request.FILES, instance=usuario)  # Prellenar con detalles

        if user_form.is_valid() and details_form.is_valid():
            user_form.save()  # Guardar cambios en el usuario
            details_form.save()  # Guardar cambios en los detalles
            messages.success(request, 'Usuario actualizado correctamente!')
            return redirect('usuarios_admin')  # Redirigir a la lista de usuarios
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        user_form = UsuarioForm(instance=usuario.user)
        details_form = DetailsUserForm(instance=usuario)

    context = {
        'usuario': usuario,
        'user_form': user_form,
        'details_form': details_form,
    }
    return render(request, 'admin/editar_usuario.html', context)

@user_passes_test(es_admin)
def detalles_usuario(request, id):
    usuario = get_object_or_404(DetailsUser, user__id=id)  # Obtener detalles del usuario por su ID

    context = {
        'usuario': usuario,
    }
    return render(request, 'admin/detalles_usuario.html', context)

@user_passes_test(es_admin)
def eliminar_usuario(request, id):
    usuario = get_object_or_404(DetailsUser, user__id=id)  # Obtener detalles del usuario por su ID

    if request.method == "POST":
        usuario.user.delete()  # Eliminar el usuario y sus detalles
        messages.success(request, 'Usuario eliminado correctamente!')
        return redirect('usuarios_admin')  # Redirigir a la lista de usuarios

    context = {
        'usuario': usuario,
    }
    return render(request, 'admin/eliminar_usuario.html', context)

def maps_views(request):
    # Obtener todos los contenedores
    containers = Container.objects.all()

    # Pasar las coordenadas de cada contenedor al contexto
    context = {
        'containers': containers,
    }

    return render(request, 'admin/maps.html', context)

def maps_location(request, location_name):
    # Obtener contenedor o ubicación específica
    containers = Container.objects.filter(location__icontains=location_name)

    # Pasar las coordenadas de cada contenedor al contexto
    context = {
        'containers': containers,
        'location_name': location_name,
    }

    return render(request, 'admin/maps.html', context)

@user_passes_test(es_admin)
def contenedores(request):
    if request.method == 'POST':
        form_container = ContainerForm(request.POST)
        form_data = TireDataForm(request.POST)
        if form_container.is_valid() and form_data.is_valid():
            # Guardar el formulario de Container
            container = form_container.save()

            # Crear el objeto TireData y asignarle el contenedor
            tire_data = form_data.save(commit=False)
            tire_data.container = container  # Asignar el contenedor al objeto TireData
            tire_data.save()  # Ahora guardar el objeto TireData

            return redirect('contenedores_admin')  # Redirigir al admin o a la página de éxito

    else:
        form_container = ContainerForm()
        form_data = TireDataForm()
        containers = Container.objects.all()
        context = {
            'contenedores': containers,
            'form_containers': form_container,
            'form_data': form_data,
        }

    return render(request, 'admin/contenedores.html', context)

@user_passes_test(es_admin)
def ver_contenedor(request, id):
    contenedor = get_object_or_404(Container, id=id)  # Obtener contenedor por ID
    context = {'contenedor': contenedor}
    return render(request, 'admin/ver_contenedor.html', context)

@user_passes_test(es_admin)
def eliminar_contenedor(request, id):
    contenedor = get_object_or_404(Container, id=id)  # Obtener contenedor por ID

    if request.method == "POST":
        contenedor.delete()  # Eliminar el contenedor
        messages.success(request, 'Contenedor eliminado correctamente!')
        return redirect('contenedores_admin')  # Redirigir a la lista de contenedores

    context = {'contenedor': contenedor}
    return render(request, 'admin/eliminar_contenedor.html', context)


@user_passes_test(es_admin)
def recoleccion(request):
    # Obtener todos los contenedores
    containers = Container.objects.all()
    
    # Pasar los contenedores al contexto
    return render(request, 'admin/recoleccion_llantas.html', {'containers': containers})

@user_passes_test(es_admin)
def tire_data_detail(request, container_id):
    # Obtener el contenedor por ID
    container = get_object_or_404(Container, id=container_id)
    
    # Obtener los datos de llantas asociados al contenedor
    tire_data = container.tire_data.all()
    
    return render(request, 'admin/tire_data_detail.html', {
        'container': container,
        'tire_data': tire_data,
    })