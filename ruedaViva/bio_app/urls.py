from django.urls import path
from bio_app.views import * # importa las vistas de la carpeta especifica
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Redirige al inicio
]