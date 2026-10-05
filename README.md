# Blog por consola

Este proyecto es un sistema de publicaciones de blog que funciona desde su consola. 
Su objetivo es organizar por partes separadas los datos, el menú, las operaciones y las validaciones del sistema.

## Funcionalidades

Desde el menú se puede:

1. Ver los posts con su título, autor y estado.
2. Buscar posts por coincidencia total o parcial en el título, sin distinguir entre mayúsculas y minúsculas.
3. Filtrar posts por coincidencia exacta de tag, también sin distinguir entre mayúsculas y minúsculas.
4. Validar la estructura de cada post y mostrar si es válido o indicar qué dato falta o es incorrecto.
5. Salir del programa.

Uno de los posts de prueba está incompleto intencionalmente para comprobar que la validación detecte la falta de contenido.

## Organización del proyecto

```text
blog_consola/
|-- main.py
|-- README.md
|-- blog/
    |-- __init__.py
    |-- datos.py
    |-- menu.py
    |-- operaciones.py
    |-- validaciones.py
```

- `main.py`: importa y coordina los scripts; inicia el menú cuando se ejecuta el programa.
- `blog/datos.py`: contiene el perfil del autor, los estados permitidos, los tags y los posts.
- `blog/menu.py`: muestra las opciones y recibe la selección del usuario.
- `blog/operaciones.py`: lista, busca y filtra los posts.
- `blog/validaciones.py`: revisa que los posts tengan la estructura y los datos requeridos.
- `blog/__init__.py`: identifica `blog` como un paquete de Python.

## Cómo ejecutar el programa

Abrí una terminal en la carpeta `blog_consola`, donde están `main.py` y la carpeta `blog`, y ejecutá:

```shell
python main.py
```

El menú aparecerá en la terminal y te pedirá que ingreses el número de la opción que quieras usar.
