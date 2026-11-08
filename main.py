from blog.datos import cargar_posts, guardar_posts, perfil_autor
from blog.menu import mostrar_menu
from blog.modelos import Autor, Blog
from blog.validaciones import validar_post


# Presenta los posts recibidos y permite personalizar el mensaje cuando la lista está vacía.
def mostrar_posts(lista_posts, mensaje_vacio = "No hay posts para mostrar."):
    if not lista_posts:
        print(mensaje_vacio)
        return

    for post in lista_posts:
        print (f"{post.id}. {post.titulo} | " f"Autor: {post.autor.nombre} | Tags: {post.tags} Estado: {post.estado}")

# Carga los posts y coordina las opciones del menú de la versión por consola.
def ejecutar_blog():
    posts_cargados, carga_completa = cargar_posts()
    blog = Blog(posts_cargados)
    
    while True:
        opcion = mostrar_menu()

        if opcion is None:
            continue
        if opcion == 1:
            mostrar_posts(blog.listar_posts())
        
        # Las búsquedas se pueden repetir hasta que el usuario escriba 0.
        elif opcion == 2:
            while True:
                termino = input("Buscar por título (0 para volver): ").strip()

                if termino == "0":
                    break
                if not termino:
                    print("La búsqueda no puede quedar vacía.")
                    continue

                mostrar_posts(
                blog.buscar_por_titulo(termino),
                "No hay posts con ese título."
                )
                
        elif opcion == 3:
            while True:
                tag = input("Filtrar por tag (0 para volver): ").strip()

                if tag == "0":
                    break
                if not tag:
                    print("El tag no puede quedar vacío.")
                    continue

                mostrar_posts(
                    blog.filtrar_por_tag(tag),
                    "No hay posts con ese tag."
                )
                
        # Solicita datos válidos antes de construir el post con el perfil registrado.
        elif opcion == 4:

            while True:
                titulo = input("Título: ").strip()
                if titulo:
                    break
                print("El Título es obligatorio.")
                
            while True:
                contenido = input("Contenido: ").strip()
                if contenido:
                    break
                print("El Contenido es obligatorio.")
                
            while True:
                nombre_autor = input("Nombre del autor: ").strip() 
                
                if nombre_autor.casefold() == perfil_autor["nombre"].casefold():
                    break

                print("Perfil no registrado, por favor ingrese un nombre registrado.")
        
            while True:
                texto_tags = input("Tags separados por comas, cada uno con # (opcional): ")
                tags = [tag.strip() for tag in texto_tags.split(",") if tag.strip()]

                if all(tag.startswith("#") and len(tag) > 1 for tag in tags):
                    break

                print("Cada tag debe comenzar con # y tener un nombre. Ejemplo: #Marvel, #MCU.")

            autor = Autor.desde_diccionario(perfil_autor)
            nuevo_post = blog.crear_post(
                autor = autor,
                titulo = titulo,
                contenido = contenido,
                tags = tags
            )
            print(f"Post {nuevo_post.id} creado como borrador.")

        elif opcion == 5:
            if not blog.listar_posts():
                print("No hay posts para validar.")
                continue
            for post in blog.listar_posts():
                es_valido, mensaje = validar_post(post)

                if es_valido:
                    print(f"Post {post.id}: válido")
                else:
                    print(f"Post {post.id}: error - {mensaje}")

        # Evita sobrescribir el JSON si su contenido anterior no se pudo cargar completo.
        elif opcion == 6:
            if not carga_completa:
                print("No se guardó: posts.json tuvo errores al cargar. Corregí el archivo y reiniciá el programa.")
                continue
            try:
                guardar_posts(blog.listar_posts())
            except (OSError, TypeError, ValueError, AttributeError) as error:
                print(f"No se pudieron guardar los posts: {error}")
            else:
                print("Posts guardados en posts.json.")

        elif opcion == 7:
            print("Gracias por usar el sistema del blog. ¡Hasta luego!")
            break

        else:
            print("Opción inválida, intentá de nuevo.")


# Inicia el menú solo cuando este archivo se ejecuta directamente.
if __name__ == "__main__":
    ejecutar_blog()
