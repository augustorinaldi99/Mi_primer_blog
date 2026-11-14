from django.test import TestCase
from django.urls import reverse

from .models import Post


class PostViewsTests(TestCase):
    # Los registros se crean en una base de prueba separada de la base local.
    @classmethod
    def setUpTestData(cls):
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
