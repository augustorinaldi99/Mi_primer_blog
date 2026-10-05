from blog.datos import posts
from blog.menu import mostrar_menu
from blog.operaciones import listar_posts, buscar_por_titulo, filtrar_por_tag
from blog.validaciones import validar_post

# Funcion para ejecutar el menu del blog y todas sus funciones.
def ejecutar_blog():
    
    while True:
        opcion = mostrar_menu()

        if opcion is None:
            continue
        elif opcion == 1:
            print("\nPosts disponibles:")
            listar_posts(posts)
        elif opcion == 2:
            termino = input("Buscar por titulo: ")
            buscar_por_titulo(posts, termino)
        elif opcion == 3:
            tag_buscado = input("Filtrar por tag: ")
            filtrar_por_tag(posts, tag_buscado)
        elif opcion == 4:
            print("\nValidación de posts:")
            for indice, post in enumerate(posts, start=1):
                es_valido, mensaje = validar_post(post)
                if es_valido:
                    print(f"Post {indice}: válido")
                else:
                    print(f"Post {indice}: error - {mensaje}")
        elif opcion == 5:
            print("Gracias por usar el sistema del blog. ¡Hasta luego!")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    ejecutar_blog()