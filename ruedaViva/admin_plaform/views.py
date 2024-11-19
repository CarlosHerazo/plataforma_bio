from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from .models import DetailsUser, Container, TireData, LlantasRecogidas
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum
import calendar

# Función para validar si el usuario es admin
def es_admin(user):
    return user.is_superuser  # Validación para administrador

@user_passes_test(es_admin)
def index_admin(request):
    # Obtener el número total de usuarios
    total_usuarios = User.objects.count()

    # Obtener el número total de centros de reciclaje (DetailsUser)
    total_centros = DetailsUser.objects.count()

    # Obtener el número total de contenedores
    total_contenedores = Container.objects.count()

   # Obtener el número total de llantas recogidas (sumando los valores de quantity_collected)
    total_llantas_recogidas = LlantasRecogidas.objects.aggregate(total=Sum('quantity_collected'))['total'] or 0
    print(total_llantas_recogidas)
    # Calcular crecimiento de usuarios en la última semana
    fecha_una_semana_atras = timezone.now() - timedelta(days=7)
    usuarios_semana_pasada = User.objects.filter(date_joined__gte=fecha_una_semana_atras).count()
    crecimiento_usuarios = (total_usuarios - usuarios_semana_pasada) / usuarios_semana_pasada * 100 if usuarios_semana_pasada > 0 else 0

    # Calcular crecimiento de contenedores en la última semana
    contenedores_semana_pasada = Container.objects.filter(created_at__gte=fecha_una_semana_atras).count()
    crecimiento_contenedores = (total_contenedores - contenedores_semana_pasada) / contenedores_semana_pasada * 100 if contenedores_semana_pasada > 0 else 0

    # Calcular crecimiento de llantas recogidas en la última semana
    llantas_recogidas_semana_pasada = LlantasRecogidas.objects.filter(date_collected__gte=fecha_una_semana_atras).aggregate(
        total=Count('quantity_collected'))['total'] or 0
    crecimiento_llantas_recogidas = (total_llantas_recogidas - llantas_recogidas_semana_pasada) / llantas_recogidas_semana_pasada * 100 if llantas_recogidas_semana_pasada > 0 else 0

    # Obtener las coordenadas de los contenedores
    contenedores = Container.objects.all().values('geo_latitude', 'geo_longitude', 'location')

    # Estimación de llantas por mes (utilizamos LlantasRecogidas si es necesario)
    llantas_por_mes = LlantasRecogidas.objects.values('date_collected__year', 'date_collected__month').annotate(
        total_llantas=Sum('quantity_collected')).order_by('date_collected__year', 'date_collected__month')

    # Agrupar las llantas recogidas por mes
    meses = [calendar.month_name[i] for i in range(1, 13)]
    estimacion_llantas = {month: 0 for month in meses}

    for data in llantas_por_mes:
        month_name = calendar.month_name[data['date_collected__month']]
        estimacion_llantas[month_name] = data['total_llantas']

    # Datos a pasar a la plantilla
    data = {
        'total_usuarios': total_usuarios,
        'total_centros': total_centros,
        'total_contenedores': total_contenedores,
        'total_llantas_recogidas': total_llantas_recogidas,  # Mostrar las llantas recogidas
        'crecimiento_usuarios': round(crecimiento_usuarios, 2),
        'crecimiento_contenedores': round(crecimiento_contenedores, 2),
        'crecimiento_llantas_recogidas': round(crecimiento_llantas_recogidas, 2),  # Crecimiento de llantas recogidas
        'contenedores': contenedores,
        'estimacion_llantas': estimacion_llantas
    }

    return render(request, "admin/index.html", data)

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
    
    
def collect_tires(request, container_id):
    container = get_object_or_404(Container, id=container_id)
    tire_data = TireData.objects.filter(container=container)

    if request.method == "POST":
        for data in tire_data:
            # Registrar la cantidad de llantas recogidas
            quantity_collected = data.quantity_to_fill  # Usamos la cantidad a llenar
            LlantasRecogidas.objects.create(
                container=container,
                tire_data=data,
                quantity_collected=quantity_collected
            )

            # Actualizar los datos en TireData
            data.current_quantity = 0  # Vaciar las llantas recogidas
            data.save()

        messages.success(request, 'Llantas recogidas exitosamente!')
        return redirect('recoleccion_admin', container_id=container.id)

    return render(request, 'collect_tires.html', {'container': container, 'tire_data': tire_data})