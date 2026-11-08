# Muestra las opciones de consola y devuelve el número elegido, si es válido.
def mostrar_menu():
    
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Crear nuevo post")
    print("5. Validar posts")
    print("6. Guardar posts en JSON")
    print("7. Salir")

    try:
        return int(input("Elegí una opción: "))
    except ValueError:
        print("Ingresá un número para elegir una opción.")
        return None
