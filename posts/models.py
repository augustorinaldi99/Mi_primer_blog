from django.conf import settings
from django.db import models

from .busqueda import normalizar_tildes


# Representa una etiqueta que puede compartirse entre publicaciones.
class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    nombre_normalizado = models.TextField(default="", editable=False)

    def save(self, *args, **kwargs):
        self.nombre_normalizado = normalizar_tildes(self.nombre)
        if kwargs.get("update_fields") is not None:
            kwargs["update_fields"] = set(kwargs["update_fields"]) | {"nombre_normalizado"}
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


# Define la publicación que Django guarda en la base de datos.
class Post(models.Model):
    # Limita los estados disponibles en el formulario de administración.
    ESTADOS = [
        ("borrador", "Borrador"),
        ("publicado", "Publicado"),
        ("archivado", "Archivado"),
    ]

    titulo = models.CharField(max_length=200)
    titulo_normalizado = models.TextField(default="", editable=False)
    contenido = models.TextField()
    autor = models.CharField(max_length=100)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="borrador",
    )
    # La imagen es opcional y se guarda en media/posts/.
    imagen = models.ImageField(upload_to="posts/", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.titulo_normalizado = normalizar_tildes(self.titulo)
        if kwargs.get("update_fields") is not None:
            kwargs["update_fields"] = set(kwargs["update_fields"]) | {"titulo_normalizado"}
        super().save(*args, **kwargs)

    # Usa el título cuando Django muestra este objeto como texto.
    def __str__(self):
        return self.titulo

    # Define los nombres visibles del modelo en el panel de administración.
    class Meta:
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"


# Guarda qué tag pertenece a cada post y en qué posición aparece.
class PostTag(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="etiquetas_ordenadas",
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    posicion = models.PositiveIntegerField()

    class Meta:
        ordering = ("posicion", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("post", "tag"),
                name="tag_unico_por_post",
            ),
            models.UniqueConstraint(
                fields=("post", "posicion"),
                name="posicion_unica_por_post",
            ),
        ]
