from django.db import models
from django.contrib.auth.models import User

class DetailsUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')
    foto_perfil = models.ImageField(upload_to='profile_pics/')
    nombre_centro = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.nombre_centro

class Container(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='containers')
    location = models.CharField(max_length=255)
    geo_latitude = models.FloatField()
    geo_longitude = models.FloatField()
    status = models.TextField(choices=[("lleno","Lleno"),("vacio","Vacio")])
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location

class TireData(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='tire_data')
    quantity_to_fill = models.IntegerField()
    current_quantity = models.IntegerField()
    alerts = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tire Data for {self.container.location}"
