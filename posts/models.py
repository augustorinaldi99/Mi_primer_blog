from django.db import models


# Define la publicación que Django guarda en la base de datos.
class Post(models.Model):
    # Limita los estados disponibles en el formulario de administración.
    ESTADOS = [
        ("borrador", "Borrador"),
        ("publicado", "Publicado"),
        ("archivado", "Archivado"),
    ]

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="borrador",
    )

    # Usa el título cuando Django muestra este objeto como texto.
    def __str__(self):
        return self.titulo

    # Define los nombres visibles del modelo en el panel de administración.
    class Meta:
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"
