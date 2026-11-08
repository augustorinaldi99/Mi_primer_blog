# Representa el perfil de un autor en la versión por consola.
class Autor: 
    # Guarda los datos del perfil; las redes sociales son opcionales.
    def __init__(self, nombre, bio, especialidad="", redes_sociales=None):
        self.nombre = nombre
        self.bio = bio
        self.especialidad = especialidad
        self.redes_sociales = redes_sociales if redes_sociales is not None else []

    # Convierte el perfil en datos que se pueden guardar en JSON.
    def a_diccionario(self):
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "especialidad" : self.especialidad,
            "redes_sociales": self.redes_sociales
        }

    # Reconstruye un autor a partir de un diccionario leído del JSON.
    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
        nombre=datos["nombre"],
        bio=datos.get("bio", ""),
        especialidad=datos.get("especialidad", ""),
        redes_sociales=datos.get("redes_sociales", [])
    )


# Representa una publicación y conserva una instancia de Autor.
class Post:

    estados_post = ("borrador", "archivado", "publicado")
    estado_post_default = "borrador"
    
    # Inicializa una publicación; los tags y el contenido pueden empezar vacíos.
    def __init__(self, id, autor, titulo="", contenido = "", tags=None, estado=estado_post_default):
        self.id = int(id)
        self.titulo = titulo
        self.contenido = contenido 
        self.autor = autor
        self.tags = tags if tags is not None else []
        self.estado = estado

    # Convierte también el autor para que el post completo se pueda guardar en JSON.
    def a_diccionario(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.a_diccionario(),
            "tags": self.tags,
            "estado": self.estado
        }

    # Reconstruye el post y su autor desde los datos almacenados.
    @classmethod
    def desde_diccionario(cls, datos):
        autor = Autor.desde_diccionario(datos["autor"])

        return cls(
            id=datos["id"],
            autor=autor,
            titulo=datos.get("titulo", ""),
            contenido=datos.get("contenido", ""),
            tags=datos.get("tags", []),
            estado=datos.get("estado", cls.estado_post_default)
        )
        
# Reúne los posts y las operaciones de búsqueda y creación del blog de consola.
class Blog:

    # Inicia el blog con los posts cargados o con una lista nueva.
    def __init__(self, posts=None):
        self.posts = posts if posts is not None else []

    # Devuelve las publicaciones disponibles en memoria.
    def listar_posts(self):
        return self.posts

    # Busca coincidencias parciales sin distinguir mayúsculas de minúsculas.
    def buscar_por_titulo(self, termino):
        termino = termino.strip().lower()

        if not termino:
            return[]

        resultados = []

        for post in self.posts:
            if termino in post.titulo.lower():
                resultados.append(post)

        return resultados

    # Compara tags ignorando espacios, mayúsculas y el símbolo # inicial.
    def filtrar_por_tag (self, tag_buscado):
        tag_buscado = tag_buscado.strip().lower().replace(" ","").lstrip("#")

        if not tag_buscado:
            return []

        resultados = []

        for post in self.posts:
            for tag in post.tags:
                tag_normalizado = tag.strip().lower().replace(" ","").lstrip("#")

                if tag_buscado in tag_normalizado:
                    resultados.append(post)
                    break

        return resultados

    # Asigna el próximo ID disponible y agrega una publicación al blog.
    def crear_post(self, autor, titulo, contenido="", tags=None, estado=Post.estado_post_default):
        nuevo_id = 1

        for post in self.posts:
            if post.id >= nuevo_id:
                nuevo_id = post.id + 1

        nuevo_post = Post (
            id = nuevo_id, 
            autor = autor,
            titulo = titulo,
            contenido = contenido,
            tags = tags, 
            estado = estado
        )

        self.posts.append(nuevo_post)
        return nuevo_post

