from django.urls import path
from bio_app.views import * # importa las vistas de la carpeta especifica
urlpatterns = [
    path('', login, name="login"),
]