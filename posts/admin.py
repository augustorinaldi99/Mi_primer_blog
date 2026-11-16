from django import forms
from django.contrib import admin

from .forms import PostForm
from .models import Post


# Usa en Administración la misma validación de tags que en Gestión.
class AdminPostForm(PostForm):
    modificar_tags = forms.BooleanField(
        label="Modificar tags",
        required=False,
    )

    def clean_tags_texto(self):
        if not self.cleaned_data.get("modificar_tags"):
            return []
        return super().clean_tags_texto()

    class Media:
        js = ("posts/js/admin_tags.js",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = AdminPostForm
    fields = (
        "titulo",
        "contenido",
        "estado",
        "imagen",
        "modificar_tags",
        "tags_texto",
    )
    list_display = ("titulo", "autor", "estado", "fecha_creacion")

    # Al crear desde Administración, asigna la cuenta como en Gestión.
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
            obj.autor = request.user.get_full_name() or request.user.get_username()
        super().save_model(request, obj, form, change)

    # Solo cambia las etiquetas si se marcó la casilla.
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if form.cleaned_data.get("modificar_tags"):
            form.guardar_tags(form.instance)
