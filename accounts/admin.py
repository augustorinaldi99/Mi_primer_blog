from django.contrib import admin

from .models import Perfil


# Permite consultar y editar perfiles desde el panel de administración.
admin.site.register(Perfil)