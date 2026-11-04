import json 
from pathlib import Path
from blog.modelos import Post

perfil_autor = {
    "nombre": "Augusto Rinaldi",
    "bio": "Crítico de películas",
    "especialidad": "Universo de superhéroes",
    "redes_sociales": [
        "@augustorinaldi",
        "@augustorinaldi_movies",
        "@augustorinaldi_moives.ok"
    ]
}

posts = [
    {
        "id": 1,
        "titulo": "Qué es el MCU",
        "contenido": "Explicación del Universo Cinematográfico de Marvel.",
        "autor": perfil_autor,
        "tags": ["#Marvel", "#Avengers", "#MCU"],
        "estado": "publicado"
    },
    {
        "id": 2,
        "titulo": "Explicación del Multiverso",
        "contenido": "Una explicación de distintas realidades y líneas temporales.",
        "autor": perfil_autor,
        "tags": ["#Multiverso", "#Timeline", "#Spiderverse"],
        "estado": "borrador"
    },
    {
        "id": 3,
        "titulo": "Top 10 personajes más poderosos",
        "contenido": "Un listado de personajes poderosos del universo Marvel.",
        "autor": perfil_autor,
        "tags": ["#Thor", "#DoctorDoom", "#Wanda"],
        "estado": "archivado"
    },
    {
        "id": 4,
        "titulo": "Post incompleto para probar la validación",
        "autor": perfil_autor,
        "tags": ["#Testeo"],
        "estado": "borrador"
    }
]

RUTA_POST = Path(__file__).resolve().parent.parent / "posts.json"

def guardar_posts(lista_posts):
    datos = [post.a_diccionario() for post in lista_posts]

    with RUTA_POST.open("w", encoding = "utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii = False, indent = 4)

def cargar_posts():
    if not RUTA_POST.exists():
        print("posts.json no existe; el blog comenzará vacío.")
        return [], True

    try:
        with RUTA_POST.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (OSError, json.JSONDecodeError) as error:
        print(f"No fue posible leer el archivo 'posts.json': {error}")
        return[],False

    if not isinstance(datos, list):
        print("El archivo 'posts.json' debe contener una lista de posts.")
        return[], False

    posts_cargados = []
    hubo_error = False

    for numero, dato in enumerate(datos, start=1):
        try:
            post = Post.desde_diccionario(dato)

            if not isinstance(post.titulo, str):
                raise ValueError("el título debe ser texto")
            if not isinstance(post.contenido, str):
                raise ValueError("el contenido debe ser texto")
            if not isinstance(post.autor.nombre, str):
                raise ValueError("el nombre del autor debe ser texto")
            if not isinstance(post.tags, list) or not all(
                isinstance(tag, str) for tag in post.tags
            ):
                raise ValueError("los tags deben ser una lista de textos")

            posts_cargados.append(post)
        except (KeyError, TypeError, ValueError, AttributeError) as error:
            hubo_error = True 
            print(f"No se pudo cargar el post {numero}: {error}")

    return posts_cargados, not hubo_error