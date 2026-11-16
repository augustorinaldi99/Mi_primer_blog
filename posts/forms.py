from django import forms
from django.db import transaction

from .models import Post, PostTag, Tag


# Recibe los tags como texto y los convierte en etiquetas del post.
class PostForm(forms.ModelForm):
    tags_texto = forms.CharField(
        label="Tags",
        required=False,
        help_text="Separados por comas. Ejemplo: #Marvel, #MCU",
    )

    class Meta:
        model = Post
        fields = ("titulo", "contenido", "estado", "imagen", "tags_texto")

    # Al editar, muestra los tags que el post ya tiene.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["tags_texto"].initial = ", ".join(
                vinculo.tag.nombre
                for vinculo in self.instance.etiquetas_ordenadas.select_related("tag")
            )

    # Comprueba el formato antes de guardar nada.
    def clean_tags_texto(self):
        texto = self.cleaned_data["tags_texto"]
        nombres = [nombre.strip() for nombre in texto.split(",") if nombre.strip()]

        for nombre in nombres:
            if not nombre.startswith("#") or len(nombre) == 1:
                raise forms.ValidationError(
                    "Cada tag debe comenzar con # y tener un nombre."
                )
            if len(nombre) > 50:
                raise forms.ValidationError("Cada tag admite hasta 50 caracteres.")
            if any(caracter.isspace() for caracter in nombre):
                raise forms.ValidationError(
                    "Los tags no pueden contener espacios; separalos con comas."
                )

        return nombres

    # Guarda las etiquetas en el mismo orden en que fueron escritas.
    def guardar_tags(self, post):
        with transaction.atomic():
            PostTag.objects.filter(post=post).delete()
            usados = set()
            posicion = 0

            for nombre in self.cleaned_data["tags_texto"]:
                tag = Tag.objects.filter(nombre__iexact=nombre).first()
                if tag is None:
                    tag = Tag.objects.create(nombre=nombre)

                if tag.pk in usados:
                    continue

                PostTag.objects.create(
                    post=post,
                    tag=tag,
                    posicion=posicion,
                )
                usados.add(tag.pk)
                posicion += 1
