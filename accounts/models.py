from django.conf import settings
from django.db import models

# Agrega biografía y avatar al usuario de Django.
class Perfil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    biografia = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatares/", blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.get_username()}"