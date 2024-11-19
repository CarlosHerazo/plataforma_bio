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
    quantity_to_fill = models.IntegerField(null=True)
    current_quantity = models.IntegerField(null=True)
    quantity_ml = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    alerts = models.TextField(null=True)
    status = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tire Data for {self.container.location}"


class LlantasRecogidas(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='llantas_recogidas')
    tire_data = models.ForeignKey(TireData, on_delete=models.CASCADE, related_name='llantas_recogidas')
    quantity_collected = models.IntegerField()  # Cantidad de llantas recogidas
    date_collected = models.DateTimeField(auto_now_add=True)  # Fecha de recolección

    def __str__(self):
        return f"Llantas recogidas en {self.container.location} - {self.quantity_collected} llantas"