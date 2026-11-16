from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Post, PostTag, Tag


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
            titulo="Post público",
            contenido="Contenido visible",
            autor="Augusto",
            estado="publicado",
            creado_por=cls.usuario,
        )
        cls.borrador = Post.objects.create(
            titulo="Post privado",
            contenido="Contenido de prueba",
            autor="Augusto",
            estado="borrador",
            creado_por=cls.usuario,
        )
        cls.archivado = Post.objects.create(
            titulo="Post archivado",
            contenido="Contenido anterior",
            autor="Augusto",
            estado="archivado",
            creado_por=cls.usuario,
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

    # Otro usuario no puede ver en Gestión ni modificar un post ajeno.
    def test_otro_usuario_no_puede_modificar_post_ajeno(self):
        otro_usuario = get_user_model().objects.create_user(
            username="otro_editor", password="clave-de-prueba-456"
        )
        self.client.force_login(otro_usuario)

        gestion = self.client.get(reverse("posts:gestion_posts"))
        self.assertEqual(list(gestion.context["posts"]), [])

        url_editar = reverse("posts:editar_post", args=[self.borrador.id])
        url_eliminar = reverse("posts:eliminar_post", args=[self.borrador.id])

        self.assertEqual(self.client.get(url_editar).status_code, 403)
        self.assertEqual(self.client.post(url_editar).status_code, 403)
        self.assertEqual(self.client.get(url_eliminar).status_code, 403)
        self.assertEqual(self.client.post(url_eliminar).status_code, 403)

        self.borrador.refresh_from_db()
        self.assertEqual(self.borrador.titulo, "Post privado")

    # Conserva el orden de los tags después de editar un post.
    def test_editar_post_conserva_orden_de_tags(self):
        self.client.force_login(self.usuario)
        url = reverse("posts:editar_post", args=[self.publicado.id])

        datos = {
            "titulo": self.publicado.titulo,
            "contenido": self.publicado.contenido,
            "estado": "publicado",
            "tags_texto": "#Marvel, #MCU",
        }
        self.assertRedirects(self.client.post(url, datos), reverse("posts:gestion_posts"))

        datos["tags_texto"] = "#MCU, #Marvel"
        self.assertRedirects(self.client.post(url, datos), reverse("posts:gestion_posts"))

        nombres = [
            vinculo.tag.nombre
            for vinculo in self.publicado.etiquetas_ordenadas.select_related("tag")
        ]
        self.assertEqual(nombres, ["#MCU", "#Marvel"])

        inicio = self.client.get(reverse("posts:inicio")).content.decode()
        self.assertLess(inicio.index("#MCU"), inicio.index("#Marvel"))

    # Solo el dueño puede ver la vista previa de borradores y archivados.
    def test_vista_previa_solo_para_dueno(self):
        urls = [
            reverse("posts:vista_previa_post", args=[self.borrador.id]),
            reverse("posts:vista_previa_post", args=[self.archivado.id]),
        ]

        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 302)

        self.client.force_login(self.usuario)
        for url in urls:
            respuesta = self.client.get(url)
            self.assertEqual(respuesta.status_code, 200)
            self.assertContains(respuesta, "Vista previa privada")

        otro_usuario = get_user_model().objects.create_user(
            username="lector_de_prueba",
            password="clave-de-prueba-789",
        )
        self.client.force_login(otro_usuario)
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 403)

    # La búsqueda encuentra títulos con o sin tildes, también después de editarlos.
    def test_busqueda_titulo_ignora_tildes(self):
        post = Post.objects.create(
            titulo="Qué hay de nuevo",
            contenido="Contenido de prueba",
            autor="Augusto",
            estado="publicado",
            creado_por=self.usuario,
        )

        respuesta = self.client.get(reverse("posts:inicio"), {"q": "QUE"})
        self.assertEqual(list(respuesta.context["posts"]), [post])

        post.titulo = "Héroe cósmico"
        post.save(update_fields={"titulo"})
        respuesta = self.client.get(reverse("posts:inicio"), {"q": "heroe"})
        self.assertEqual(list(respuesta.context["posts"]), [post])

        respuesta = self.client.get(reverse("posts:inicio"), {"q": "inexistente"})
        self.assertContains(respuesta, "No se encontraron publicaciones")

    # El tag puede buscarse sin tildes, sin distinguir mayúsculas ni espacios.
    def test_busqueda_tag_ignora_tildes_y_espacios(self):
        tag = Tag.objects.create(nombre="#HéroeCósmico")
        PostTag.objects.create(post=self.publicado, tag=tag, posicion=0)

        respuesta = self.client.get(
            reverse("posts:inicio"), {"q": "#heroe cosmico"}
        )
        self.assertEqual(list(respuesta.context["posts"]), [self.publicado])

    # Quitar tildes no debe confundir la ñ con la n.
    def test_busqueda_distingue_enye(self):
        post = Post.objects.create(
            titulo="Año especial",
            contenido="Contenido de prueba",
            autor="Augusto",
            estado="publicado",
            creado_por=self.usuario,
        )

        respuesta = self.client.get(reverse("posts:inicio"), {"q": "ano"})
        self.assertNotIn(post, list(respuesta.context["posts"]))
        respuesta = self.client.get(reverse("posts:inicio"), {"q": "año"})
        self.assertIn(post, list(respuesta.context["posts"]))

    # El enlace de un tag exige coincidencia exacta y oculta los borradores.
    def test_pagina_de_tag_filtra_publicados_y_coincidencia_exacta(self):
        tag = Tag.objects.create(nombre="#Marvel")
        parecido = Tag.objects.create(nombre="#MarvelExtra")
        PostTag.objects.create(post=self.publicado, tag=tag, posicion=0)
        PostTag.objects.create(post=self.borrador, tag=tag, posicion=0)
        otro_post = Post.objects.create(
            titulo="Otra publicación",
            contenido="Contenido de prueba",
            autor="Augusto",
            estado="publicado",
            creado_por=self.usuario,
        )
        PostTag.objects.create(post=otro_post, tag=parecido, posicion=0)

        url = reverse("posts:posts_por_tag", args=[tag.pk])
        respuesta = self.client.get(url)
        self.assertEqual(list(respuesta.context["posts"]), [self.publicado])
        self.assertContains(respuesta, tag.nombre)
        self.assertEqual(
            self.client.get(reverse("posts:posts_por_tag", args=[9999])).status_code,
            404,
        )

    # Inicio reparte cuatro publicaciones en páginas de tres y una.
    def test_paginacion_inicio(self):
        for numero in range(3):
            Post.objects.create(
                titulo=f"Publicación {numero}",
                contenido="Contenido de prueba",
                autor="Augusto",
                estado="publicado",
                creado_por=self.usuario,
            )

        primera = self.client.get(reverse("posts:inicio"))
        segunda = self.client.get(reverse("posts:inicio"), {"page": 2})
        self.assertEqual(len(list(primera.context["posts"])), 3)
        self.assertEqual(list(segunda.context["posts"]), [self.publicado])
        self.assertEqual(primera.context["pagina"].paginator.num_pages, 2)
        self.assertContains(primera, "page=2")

    # Al pasar de página, la búsqueda conserva el término ingresado.
    def test_paginacion_busqueda_conserva_termino(self):
        for numero in range(4):
            Post.objects.create(
                titulo=f"Héroe {numero}",
                contenido="Contenido de prueba",
                autor="Augusto",
                estado="publicado",
                creado_por=self.usuario,
            )

        url = reverse("posts:inicio")
        primera = self.client.get(url, {"q": "heroe"})
        segunda = self.client.get(url, {"q": "heroe", "page": 2})
        self.assertEqual(len(list(primera.context["posts"])), 3)
        self.assertEqual(len(list(segunda.context["posts"])), 1)
        self.assertContains(primera, "q=heroe&amp;page=2")

    # Las páginas de un tag usan el mismo límite de tres posts.
    def test_paginacion_de_tag(self):
        tag = Tag.objects.create(nombre="#Equipo")
        for numero in range(4):
            post = Post.objects.create(
                titulo=f"Miembro {numero}",
                contenido="Contenido de prueba",
                autor="Augusto",
                estado="publicado",
                creado_por=self.usuario,
            )
            PostTag.objects.create(post=post, tag=tag, posicion=0)

        url = reverse("posts:posts_por_tag", args=[tag.pk])
        primera = self.client.get(url)
        segunda = self.client.get(url, {"page": 2})
        self.assertEqual(len(list(primera.context["posts"])), 3)
        self.assertEqual(len(list(segunda.context["posts"])), 1)

    # Administración y Gestión leen los tags en el mismo orden guardado.
    def test_tags_editados_en_admin_aparecen_en_gestion(self):
        administrador = get_user_model().objects.create_superuser(
            username="administrador",
            email="admin@example.com",
            password="ClaveDePruebaLarga123!",
        )
        self.client.force_login(administrador)
        respuesta = self.client.post(
            reverse("admin:posts_post_change", args=[self.publicado.pk]),
            {
                "titulo": self.publicado.titulo,
                "contenido": self.publicado.contenido,
                "estado": "publicado",
                "modificar_tags": "on",
                "tags_texto": "#Segundo, #Primero",
            },
        )
        self.assertEqual(respuesta.status_code, 302)

        self.client.force_login(self.usuario)
        respuesta = self.client.get(
            reverse("posts:editar_post", args=[self.publicado.pk])
        )
        self.assertEqual(
            respuesta.context["form"]["tags_texto"].value(),
            "#Segundo, #Primero",
        )

    # Un tag sin # no crea el post y deja el error en el formulario.
    def test_crear_post_rechaza_tag_sin_numeral(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(
            reverse("posts:crear_post"),
            {
                "titulo": "Post inválido",
                "contenido": "Contenido de prueba",
                "estado": "publicado",
                "tags_texto": "Marvel",
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertFormError(
            respuesta.context["form"],
            "tags_texto",
            "Cada tag debe comenzar con # y tener un nombre.",
        )
        self.assertFalse(Post.objects.filter(titulo="Post inválido").exists())
