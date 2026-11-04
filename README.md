# Mi primer blog: versión por consola

Este proyecto permite administrar publicaciones desde un menú en la terminal. En esta preentrega, el blog usa clases para representar autores y posts, y guarda las publicaciones en `posts.json` para recuperarlas en la siguiente ejecución.

## Cómo ejecutarlo

Se necesita Python. Abrí una terminal en la carpeta que contiene `main.py` y ejecutá:

```shell
python main.py
```

Al iniciar, el programa carga los posts de `posts.json` y muestra el menú. La opción **6. Guardar posts en JSON** guarda los cambios: salir con la opción 7 no los guarda automáticamente.

## Opciones del menú

1. **Ver todos los posts:** muestra el ID, el título, el autor, los tags y el estado de cada publicación cargada.
2. **Buscar por título:** encuentra coincidencias totales o parciales sin distinguir mayúsculas de minúsculas. Permite repetir la búsqueda; `0` vuelve al menú.
3. **Filtrar por tag:** encuentra coincidencias parciales sin distinguir mayúsculas de minúsculas; también ignora el `#` inicial y los espacios al comparar. Permite repetir el filtrado; `0` vuelve al menú.
4. **Crear nuevo post:** pide título y contenido, y vuelve a preguntar si alguno está vacío. Después pide el nombre del autor registrado en `blog/datos.py` y tags opcionales separados por comas. Cada tag ingresado debe comenzar con `#`. El post recibe un ID nuevo y comienza en estado `borrador`.
5. **Validar posts:** informa si cada publicación tiene los datos requeridos o qué dato es incorrecto. Hay un post de prueba sin contenido para comprobar esta función.
6. **Guardar posts en JSON:** escribe los posts actuales en `posts.json`.
7. **Salir:** termina el programa.

## Clases y organización

Los archivos principales de la versión por consola son:

```text
.
├── main.py
├── posts.json
└── blog/
    ├── __init__.py
    ├── datos.py
    ├── menu.py
    ├── modelos.py
    └── validaciones.py
```

- **`Autor`:** guarda nombre, bio, especialidad y redes sociales. Al crear un post se construye un objeto `Autor` a partir del perfil registrado.
- **`Post`:** guarda ID, título, contenido, tags, estado y un objeto `Autor`.
- **`Blog`:** mantiene la lista de objetos `Post` y ofrece métodos para listarlos, buscarlos por título, filtrarlos por tag y crear nuevos posts.
- **`main.py`:** carga los datos, crea la instancia de `Blog` y conecta sus métodos con el menú.
- **`blog/menu.py`:** muestra las opciones y lee la elección del usuario.
- **`blog/validaciones.py`:** revisa los datos de cada objeto `Post`.
- **`blog/datos.py`:** define el perfil de autor registrado y las funciones para cargar y guardar `posts.json`.

## Cómo funciona `posts.json`

Al guardar, cada objeto `Post` se convierte en un diccionario; su objeto `Autor` también se convierte en un diccionario. Python escribe la lista resultante en `posts.json`. Al volver a ejecutar el programa, `blog/datos.py` lee el archivo y reconstruye los objetos `Autor` y `Post` antes de crear el `Blog`.

El archivo debe contener una lista de posts. Si `posts.json` no existe, el blog empieza vacío y se puede crear y guardar un post nuevo. Si el archivo no se puede leer o alguno de sus posts tiene datos de un tipo incorrecto, el programa informa el error y permite consultar los posts que sí pudo recuperar.

Cuando hubo un error de carga, la opción 6 bloquea el guardado para evitar que una lista vacía o incompleta reemplace el archivo original. En ese caso, corregí `posts.json` y reiniciá el programa antes de guardar.

## Cambio respecto de la preentrega anterior

Antes, el programa trabajaba principalmente con diccionarios y funciones separadas. Ahora trabaja con objetos `Autor`, `Post` y `Blog`, concentra las operaciones sobre publicaciones en la clase `Blog` y conserva los posts entre ejecuciones mediante `posts.json`.
