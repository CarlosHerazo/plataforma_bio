from django.urls import path
from admin_plaform.views import * # importa las vistas de la carpeta especifica
urlpatterns = [
    path('', index_admin, name="admin_only"),
    path('users/', usuarios, name="usuarios_admin"),
     path('user/editar/<int:id>/', editar_usuario, name='usuario_editar'),
    path('user/detalles/<int:id>/', detalles_usuario, name='usuario_detalles'),
    path('user/eliminar/<int:id>/', eliminar_usuario, name='usuario_eliminar'),
    path('containers/', contenedores, name="contenedores_admin"),
     path('container/ver/<int:id>/', ver_contenedor, name='contenedor_ver'),
    path('container/eliminar/<int:id>/', eliminar_contenedor, name='contenedor_eliminar'),
    path('recoleccion/', recoleccion, name="recoleccion_admin"),
    path('recoleccion/tire_data/<int:container_id>/', tire_data_detail, name='tire_data_detail'),
    path('maps/', maps_views, name="maps"),
    path('maps/<str:location_name>/', maps_location, name='maps_location'),  # Ruta para ver el mapa con parámetro
]