import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from blog.datos import cargar_posts, guardar_posts
from blog.modelos import Autor, Blog


class BlogConsolaTests(unittest.TestCase):
    # Prepara un blog independiente para cada prueba.
    def setUp(self):
        self.autor = Autor("Augusto", "Crítico de cine")
        self.blog = Blog()

    # Comprueba que los IDs crecen y el estado inicial es borrador.
    def test_crear_post(self):
        primero = self.blog.crear_post(self.autor, "Primer post")
        segundo = self.blog.crear_post(self.autor, "Segundo post")

        self.assertEqual([primero.id, segundo.id], [1, 2])
        self.assertEqual(primero.estado, "borrador")
        self.assertEqual(self.blog.listar_posts(), [primero, segundo])

    # La búsqueda debe admitir partes del título sin distinguir mayúsculas.
    def test_buscar_por_titulo(self):
        esperado = self.blog.crear_post(self.autor, "Qué es el MCU")
        self.blog.crear_post(self.autor, "Django para principiantes")

        self.assertEqual(self.blog.buscar_por_titulo("mCu"), [esperado])
        self.assertEqual(self.blog.buscar_por_titulo("  "), [])

    # El filtro admite espacios y # en la búsqueda de un tag.
    def test_filtrar_por_tag(self):
        esperado = self.blog.crear_post(self.autor, "Personajes", tags=["#DoctorDoom"])
        self.blog.crear_post(self.autor, "Otro post", tags=["#SpiderMan"])

        self.assertEqual(self.blog.filtrar_por_tag("doctor doom"), [esperado])
        self.assertEqual(self.blog.filtrar_por_tag("#DOCTORDOOM"), [esperado])

    # El JSON temporal debe reconstruir el post y su objeto Autor.
    def test_guardar_y_cargar_json(self):
        original = self.blog.crear_post(
            self.autor, "Post de prueba", "Contenido", tags=["#Marvel"]
        )

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "posts.json"
            with patch("blog.datos.RUTA_POST", ruta):
                guardar_posts(self.blog.listar_posts())
                recuperados, carga_completa = cargar_posts()

        self.assertTrue(carga_completa)
        self.assertEqual(len(recuperados), 1)
        self.assertEqual(recuperados[0].id, original.id)
        self.assertEqual(recuperados[0].autor.nombre, self.autor.nombre)
        self.assertEqual(recuperados[0].tags, ["#Marvel"])


if __name__ == "__main__":
    unittest.main()
