from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Perfil


class CuentasTests(TestCase):
    # La sesión se inicia con la cuenta y se borra al enviar Cerrar sesión.
    def test_iniciar_y_cerrar_sesion(self):
        get_user_model().objects.create_user(
            username="visitante", password="ClaveDePruebaLarga123!"
        )
        respuesta = self.client.post(reverse("accounts:login"), {
            "username": "visitante",
            "password": "ClaveDePruebaLarga123!",
        })
        self.assertRedirects(respuesta, reverse("posts:inicio"))
        self.assertIn("_auth_user_id", self.client.session)

        respuesta = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(respuesta, reverse("posts:inicio"))
        self.assertNotIn("_auth_user_id", self.client.session)

    # El alta crea el perfil asociado y deja iniciada la sesión.
    def test_registro_crea_usuario_y_perfil(self):
        respuesta = self.client.post(reverse("accounts:registro"), {
            "username": "nuevo",
            "email": "nuevo@example.com",
            "password1": "ClaveDePruebaLarga123!",
            "password2": "ClaveDePruebaLarga123!",
        })

        self.assertRedirects(respuesta, reverse("posts:inicio"))
        usuario = get_user_model().objects.get(username="nuevo")
        self.assertTrue(Perfil.objects.filter(user=usuario).exists())
        self.assertEqual(int(self.client.session["_auth_user_id"]), usuario.pk)

    # Un usuario anterior a la creación de Perfil obtiene uno al visitar su página.
    def test_perfil_existente_se_puede_editar_con_avatar(self):
        usuario = get_user_model().objects.create_user(
            username="anterior", password="ClaveDePruebaLarga123!"
        )
        self.client.force_login(usuario)

        self.assertEqual(self.client.get(reverse("accounts:perfil")).status_code, 200)
        self.assertTrue(Perfil.objects.filter(user=usuario).exists())

        archivo = BytesIO()
        Image.new("RGB", (1, 1), "red").save(archivo, format="PNG")
        avatar = SimpleUploadedFile(
            "avatar.png", archivo.getvalue(), content_type="image/png"
        )

        with TemporaryDirectory() as carpeta, override_settings(MEDIA_ROOT=carpeta):
            respuesta = self.client.post(reverse("accounts:editar_perfil"), {
                "biografia": "Esta es mi biografía.",
                "avatar": avatar,
            })
            self.assertRedirects(respuesta, reverse("accounts:perfil"))
            perfil = Perfil.objects.get(user=usuario)
            self.assertEqual(perfil.biografia, "Esta es mi biografía.")
            self.assertTrue(Path(carpeta, perfil.avatar.name).is_file())
            self.assertContains(self.client.get(reverse("accounts:perfil")), perfil.avatar.url)

    # Solo la persona autenticada puede ver o modificar su propio perfil.
    def test_perfil_requiere_sesion(self):
        for nombre in ("accounts:perfil", "accounts:editar_perfil"):
            with self.subTest(nombre=nombre):
                respuesta = self.client.get(reverse(nombre))
                self.assertEqual(respuesta.status_code, 302)
                self.assertTrue(respuesta.url.startswith(reverse("accounts:login")))
