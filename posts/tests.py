from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Post


# Crea una imagen válida para probar la carga sin usar archivos del usuario.
def imagen_de_prueba(nombre):
    archivo = BytesIO()
    Image.new("RGB", (1, 1), "red").save(archivo, format="PNG")
    return SimpleUploadedFile(nombre, archivo.getvalue(), content_type="image/png")


# Comprueba las páginas públicas y las operaciones de gestión en una base aislada.
class PostViewsTests(TestCase):
    # Los registros se crean en una base de prueba separada de la base local.
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(
            username="editor", password="clave-de-prueba-123"
        )
        cls.publicado = Post.objects.create(
            titulo="Post público", contenido="Contenido visible",
            autor="Augusto", estado="publicado"
        )
        cls.borrador = Post.objects.create(
            titulo="Post privado", contenido="Contenido de prueba",
            autor="Augusto", estado="borrador"
        )
        cls.archivado = Post.objects.create(
            titulo="Post archivado", contenido="Contenido anterior",
            autor="Augusto", estado="archivado"
        )

    # El inicio debe mostrar publicaciones reales y ocultar otros estados.
    def test_inicio_muestra_solo_publicados(self):
        respuesta = self.client.get(reverse("posts:inicio"))

        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "posts/lista_posts.html")
        self.assertEqual(list(respuesta.context["posts"]), [self.publicado])
        self.assertContains(respuesta, self.publicado.titulo)
        self.assertNotContains(respuesta, self.borrador.titulo)
        self.assertNotContains(respuesta, self.archivado.titulo)

    # El detalle existe para un post publicado y no expone borradores.
    def test_detalle_restringe_estados_no_publicados(self):
        url_publicada = reverse("posts:detalle_post", args=[self.publicado.id])
        url_borrador = reverse("posts:detalle_post", args=[self.borrador.id])

        self.assertEqual(self.client.get(url_publicada).status_code, 200)
        self.assertEqual(self.client.get(url_borrador).status_code, 404)

    # La página informativa sigue disponible.
    def test_acerca_responde(self):
        self.assertEqual(self.client.get(reverse("posts:acerca")).status_code, 200)

    # Gestión muestra todos los estados, también los que no aparecen en Inicio.
    def test_gestion_muestra_todos_los_posts(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.get(reverse("posts:gestion_posts"))

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["posts"].count(), 3)
        self.assertContains(respuesta, self.borrador.titulo)
        self.assertContains(respuesta, self.archivado.titulo)

    # La creación conserva la imagen enviada y la muestra en el detalle.
    def test_crear_post_con_imagen(self):
        self.client.force_login(self.usuario)
        with TemporaryDirectory() as carpeta, override_settings(MEDIA_ROOT=carpeta):
            respuesta = self.client.post(
                reverse("posts:crear_post"),
                {
                    "titulo": "Nuevo post",
                    "contenido": "Contenido nuevo",
                    "autor": "Augusto",
                    "estado": "publicado",
                    "imagen": imagen_de_prueba("nueva.png"),
                },
            )

            self.assertRedirects(respuesta, reverse("posts:gestion_posts"))
            post = Post.objects.get(titulo="Nuevo post")
            self.assertTrue(Path(carpeta, post.imagen.name).is_file())
            detalle = self.client.get(reverse("posts:detalle_post", args=[post.id]))
            self.assertContains(detalle, post.imagen.url)

    # La edición modifica el registro existente y permite reemplazar su imagen.
    def test_editar_post_no_crea_otro_registro(self):
        self.client.force_login(self.usuario)
        with TemporaryDirectory() as carpeta, override_settings(MEDIA_ROOT=carpeta):
            respuesta = self.client.post(
                reverse("posts:editar_post", args=[self.borrador.id]),
                {
                    "titulo": "Borrador corregido",
                    "contenido": "Texto corregido",
                    "autor": "Augusto",
                    "estado": "borrador",
                    "imagen": imagen_de_prueba("reemplazo.png"),
                },
            )

            self.assertRedirects(respuesta, reverse("posts:gestion_posts"))
            self.borrador.refresh_from_db()
            self.assertEqual(self.borrador.titulo, "Borrador corregido")
            self.assertTrue(Path(carpeta, self.borrador.imagen.name).is_file())
            self.assertEqual(Post.objects.count(), 3)

    # Consultar la confirmación no borra; enviar el formulario sí.
    def test_eliminar_post_requiere_confirmacion(self):
        self.client.force_login(self.usuario)
        url = reverse("posts:eliminar_post", args=[self.borrador.id])

        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Post.objects.filter(id=self.borrador.id).exists())

        respuesta = self.client.post(url)
        self.assertRedirects(respuesta, reverse("posts:gestion_posts"))
        self.assertFalse(Post.objects.filter(id=self.borrador.id).exists())

    # Las herramientas privadas piden iniciar sesión y no modifican registros.
    def test_gestion_y_cambios_requieren_sesion(self):
        urls = [
            reverse("posts:gestion_posts"),
            reverse("posts:crear_post"),
            reverse("posts:editar_post", args=[self.borrador.id]),
            reverse("posts:eliminar_post", args=[self.borrador.id]),
        ]
        for url in urls:
            with self.subTest(url=url):
                respuesta = self.client.get(url)
                self.assertEqual(respuesta.status_code, 302)
                self.assertTrue(respuesta.url.startswith(reverse("accounts:login")))

        self.assertTrue(Post.objects.filter(id=self.borrador.id).exists())
