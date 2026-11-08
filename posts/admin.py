from django.contrib import admin
from .models import Post


# Registra el modelo y define las columnas del listado administrativo.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "estado", "fecha_creacion")
