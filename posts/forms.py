from django import forms

from .models import Post


# Reutiliza los campos y las validaciones del modelo al crear o editar posts.
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("titulo", "contenido", "autor", "estado", "imagen")
