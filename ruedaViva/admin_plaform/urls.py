from django.urls import path
from admin_plaform.views import * # importa las vistas de la carpeta especifica
urlpatterns = [
    path('', index_admin, name="admin_only"),
    path('users/', usuarios, name="usuarios_admin"),
]