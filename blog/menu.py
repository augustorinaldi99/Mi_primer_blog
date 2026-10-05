def mostrar_menu():
    
    print("\n--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Validar posts")
    print("5. Salir")

    try:
        return int(input("Elegí una opción: "))
    except ValueError:
        print("Ingresá un número para elegir una opción.")
        return None