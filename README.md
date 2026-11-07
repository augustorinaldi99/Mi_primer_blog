# Mi primer blog

Este repositorio reúne el blog por consola de la preentrega 6, la base de Django de la preentrega 7 y las primeras páginas web de la preentrega 8.

## Preentrega 8: primeras páginas web

La aplicación `posts` ofrece dos páginas: **Inicio** (`/`) y **Acerca de** (`/acerca/`). El menú permite navegar entre ellas. Ambas usan `posts/templates/posts/base.html` como estructura común y cargan el estilo desde `posts/static/posts/css/estilos.css`.

Las rutas generales están en `blog_project/urls.py`; las rutas de las dos páginas están en `posts/urls.py`. Cada ruta llama a una función de `posts/views.py`, que renderiza su template HTML. Por ahora estas páginas presentan texto de bienvenida y una descripción del autor; los posts de la versión por consola siguen en `posts.json`.

Para ver el sitio localmente, seguí los pasos de instalación y ejecución de Django que aparecen abajo y abrí `http://127.0.0.1:8000/`. También podés entrar directamente a `http://127.0.0.1:8000/acerca/`.

## Preentrega 7: base de Django

El proyecto Django se llama `blog_project` y la aplicación principal es `posts`. La app está registrada en `INSTALLED_APPS`. El idioma es español de Argentina y la zona horaria es Buenos Aires. En esa preentrega se preparó la estructura inicial; las páginas se agregaron en la preentrega 8.

### Archivos principales

```text
.
├── manage.py
├── blog_project/     # configuración general de Django
├── posts/            # aplicación inicial del blog web
├── requirements.txt
├── main.py           # versión por consola
├── posts.json        # datos de la versión por consola
└── blog/             # clases y funciones de la versión por consola
```

### Cómo ejecutar Django

Cloná el repositorio y entrá en su carpeta:

```shell
git clone https://github.com/augustorinaldi99/Mi_primer_blog.git
cd Mi_primer_blog
```

Creá el entorno virtual:

```shell
python -m venv .venv
```

Activá el entorno según tu terminal:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# Git Bash en Windows
source .venv/Scripts/activate

# Linux o macOS
source .venv/bin/activate
```

Instalá las dependencias y levantá el servidor de desarrollo:

```shell
python -m pip install -r requirements.txt
python manage.py runserver
```

Abrí `http://127.0.0.1:8000/` en el navegador. Para detener el servidor, presioná `Ctrl+C` en la terminal.

## Preentrega 6: blog por consola

Este proyecto permite administrar publicaciones desde un menú en la terminal. En la preentrega 6, el blog usa clases para representar autores y posts, y guarda las publicaciones en `posts.json` para recuperarlas en la siguiente ejecución.

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
