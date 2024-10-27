# Generated by Django 4.2.16 on 2024-10-27 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('geo_latitude', models.FloatField()),
                ('geo_longitude', models.FloatField()),
                ('status', models.TextField(choices=[('lleno', 'Lleno'), ('vacio', 'Vacio')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='containers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TireData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_to_fill', models.IntegerField()),
                ('current_quantity', models.IntegerField()),
                ('alerts', models.TextField()),
                ('status', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tire_data', to='admin_plaform.container')),
            ],
        ),
        migrations.CreateModel(
            name='DetailsUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto_perfil', models.ImageField(upload_to='profile_pics/')),
                ('nombre_centro', models.CharField(max_length=255)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
