from django.db import models


# Representa una publicación guardada en la base de datos.
class Post(models.Model):
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

    # Muestra el título de la publicación en el panel administrativo.
    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "publicación"
        verbose_name_plural = "publicaciones"
