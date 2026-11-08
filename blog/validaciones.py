from blog.modelos import Autor,Post 

# Comprueba los datos obligatorios y devuelve un resultado con su explicación.
def validar_post(post):
    
    if not isinstance(post, Post):
        return False, "Los datos del post no son válidos."

    if not isinstance(post.id, int) or post.id < 1:
        return False, "El ID debe ser un número entero positivo."

    if not isinstance(post.titulo, str) or not post.titulo.strip():
        return False, "El título no puede estar vacío."

    if not isinstance(post.contenido, str) or not post.contenido.strip():
        return False, "El contenido no puede estar vacío."

    # El autor debe ser un objeto Autor con un nombre no vacío.
    if not isinstance(post.autor, Autor):
        return False, "Los datos del autor no son válidos."

    if not isinstance(post.autor.nombre, str) or not post.autor.nombre.strip():
        return False, "El nombre del autor no puede estar vacío."

    # Los tags son opcionales, pero cada tag presente debe comenzar con #.
    if not isinstance(post.tags, list):
        return False, "Los tags deben estar en formato lista."

    for tag in post.tags:
        if not isinstance(tag, str) or not tag.strip():
            return False, "La lista de tags contiene un valor inválido."

        if not tag.strip().startswith("#") or len(tag.strip()) == 1:
            return False, "Cada tag debe comenzar con # y tener un nombre."

    if post.estado not in Post.estados_post:
        return False, "El estado del post no es válido."

    return True, "Válido."
