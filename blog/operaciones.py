# Muestra la lista de posts del blog.
def listar_posts(lista):
    
    if not lista:
        print("No hay posts para mostrar.")
        return

    for post in lista:
        if not isinstance(post, dict):
            print("- Post inválido: no es un diccionario.")
            continue

        titulo = post.get("titulo", "(sin título)")
        autor = post.get("autor")
        estado = post.get("estado")
        if isinstance(autor, dict):
            nombre_autor = autor.get("nombre", "(sin nombre)")
        else:
            nombre_autor = "(autor inválido)"

        print(f"- {titulo} | Autor: {nombre_autor} | Estado: {estado}")

# Muestra los posts cuyo título contiene el término buscado.
def buscar_por_titulo(lista, termino):
    
    termino = termino.strip().lower()
    if not termino:
        print("La búsqueda no puede quedar vacía.")
        return

    resultados = []
    for post in lista:
        if not isinstance(post, dict):
            continue
        titulo = post.get("titulo")
        if isinstance(titulo, str) and termino in titulo.lower():
            resultados.append(post)

    if resultados:
        print("\nResultados de búsqueda:")
        listar_posts(resultados)
    else:
        print("No se encontraron posts con ese título.")

# Muestra los posts que contienen el tag indicado, sin distinguir mayúsculas.
def filtrar_por_tag(lista, tag_buscado):
    
    tag_buscado = tag_buscado.strip().lower()
    if not tag_buscado:
        print("El tag no puede quedar vacío.")
        return

    resultados = []
    for post in lista:
        if not isinstance(post, dict):
            continue
        tags_post = post.get("tags")
        if not isinstance(tags_post, list):
            continue

        for tag in tags_post:
            if isinstance(tag, str) and tag_buscado == tag.strip().lower():
                resultados.append(post)
                break

    if resultados:
        print("\nPosts con ese tag:")
        listar_posts(resultados)
    else:
        print("No se encontraron posts con ese tag.")