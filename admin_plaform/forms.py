from django import forms
from django.contrib.auth.models import User
from .models import Container, TireData
from django.contrib.auth.hashers import make_password
from .models import DetailsUser

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user

class DetailsUserForm(forms.ModelForm):
    class Meta:
        model = DetailsUser
        fields = ['foto_perfil', 'nombre_centro', 'direccion', 'telefono']

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ['user', 'location', 'geo_latitude', 'geo_longitude', 'status']

class TireDataForm(forms.ModelForm):
    class Meta:
        model = TireData
        fields = ['quantity_to_fill']

