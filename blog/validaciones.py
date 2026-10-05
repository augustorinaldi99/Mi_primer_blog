from blog.datos import estados_post 

# Funcion para validar los posts del blog
def validar_post(post):
    
    if not isinstance(post, dict):
        return False, "el post no es un diccionario"

    claves_obligatorias = ("id", "titulo", "contenido", "autor", "tags", "estado")
    for clave in claves_obligatorias:
        if clave not in post:
            return False, f'Falta la clave "{clave}".'

    titulo = post.get("titulo")
    if not isinstance(titulo, str) or not titulo.strip():
        return False, "El título no puede estar vacio."

    contenido = post.get("contenido")
    if not isinstance(contenido, str) or not contenido.strip():
        return False, "El contenido no puede estar vacío."

    autor = post.get("autor")
    if not isinstance(autor, dict):
        return False, "El autor no es un diccionario."
    nombre_autor = autor.get("nombre")
    if not isinstance(nombre_autor, str) or not nombre_autor.strip():
        return False, 'Falta un nombre de autor válido en la clave "nombre".'

    tags_post = post.get("tags")
    if not isinstance(tags_post, list):
        return False, 'La clave "tags" no contiene una lista'
    for tag in tags_post:
        if not isinstance(tag, str) or not tag.strip():
            return False, "La lista de tags contiene un valor inválido."

    if post.get("estado") not in estados_post:
        return False, "El estado ingresado no es valido."

    return True, "Válido."