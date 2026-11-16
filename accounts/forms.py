from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Perfil


# Agrega el correo al formulario de creación de usuarios de Django.
class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")


# Permite cambiar únicamente los datos adicionales del perfil.
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ("biografia", "avatar")
