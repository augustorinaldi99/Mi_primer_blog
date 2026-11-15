# Mi primer blog

Este repositorio reúne el blog por consola de la preentrega 6 y su evolución web en Django hasta la preentrega 10.

## Versiones necesarias

Este proyecto usa Django 6.1.2, compatible con Python 3.12, 3.13 y 3.14. Se probó localmente con Python 3.14.7. Las versiones de los paquetes externos se fijan en `requirements.txt`. Antes de crear el entorno virtual, comprobá tu Python con `python --version`.

Para ejecutar el proyecto en otro equipo, creá un entorno virtual, instalá `requirements.txt` y aplicá las migraciones. La base de datos local no se incluye en Git; después podés cargar posts desde la página de Gestión o crear un superusuario para usar `/admin/`.

## Preentrega 10: gestión de posts e imágenes

La página pública (`/`) muestra solo los posts publicados. Desde **Gestión** (`/gestion/`) se ven todos los estados y se puede crear, editar o eliminar una publicación. La eliminación pide confirmación: abrir esa página no borra el post; el borrado ocurre al enviar el formulario. El administrador de Django sigue disponible en `/admin/`.

`posts/forms.py` define `PostForm` a partir del modelo `Post`. El mismo formulario se usa para crear y editar título, contenido, autor, estado e imagen. Los formularios envían la imagen con `enctype="multipart/form-data"`; las vistas la reciben mediante `request.FILES`. Esta preentrega no incluye autenticación ni permisos para Gestión.

Pillow, fijado en `requirements.txt`, permite validar los archivos del campo `ImageField`. Django guarda las imágenes subidas en `media/posts/` (`MEDIA_ROOT`) y registra su ruta relativa en la base de datos. `MEDIA_URL` y las rutas del proyecto permiten verlas con el servidor de desarrollo. La imagen se muestra en el detalle del post cuando existe; el listado público conserva solo el texto de adelanto. La carpeta `media/` y la base `db.sqlite3` son datos locales ignorados por Git: al clonar el proyecto, hay que crear las publicaciones y subir sus imágenes desde el formulario.

Para probar el flujo: iniciá el servidor, entrá en `/gestion/`, creá un post publicado con una imagen y abrí su detalle desde Inicio. Después editá el post para cambiar la imagen, probá **Cancelar** en la confirmación de borrado y, con un post de prueba, confirmá la eliminación. En una instalación nueva, aplicá las migraciones antes de usar el formulario.

## Preentrega 9: publicaciones en Django

La aplicación `posts` tiene un modelo `Post` con título, contenido, autor, fecha de creación y estado (`borrador`, `publicado` o `archivado`). Las migraciones crean su tabla en SQLite. El modelo está registrado en el administrador de Django, donde se pueden crear publicaciones y ver sus datos en una lista.

Para preparar la base de datos y crear un usuario administrador, después de instalar las dependencias ejecutá:

```shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Entrá a `http://127.0.0.1:8000/admin/` con ese usuario y creá al menos tres publicaciones, incluida una con estado `publicado`. La página de inicio (`/`) consulta la base de datos y muestra solamente las publicadas, ordenadas de la más reciente a la más antigua. Cada título abre el contenido completo en `/posts/<id>/`; el inicio muestra un adelanto de 50 palabras. Los borradores y los posts archivados no aparecen en la página pública.

`db.sqlite3` y las credenciales del administrador son locales y no se suben al repositorio. Por eso, al clonar el proyecto, hay que aplicar las migraciones y cargar publicaciones desde `/admin/` para verlas en el sitio. La versión por consola conserva sus datos por separado en `posts.json`.

## Preentrega 8: primeras páginas web

La aplicación `posts` ofrece dos páginas: **Inicio** (`/`) y **Acerca de** (`/acerca/`). El menú permite navegar entre ellas. Ambas usan `posts/templates/posts/base.html` como estructura común y cargan el estilo desde `posts/static/posts/css/estilos.css`.

Las rutas generales están en `blog_project/urls.py`; las rutas de las páginas están en `posts/urls.py`. Cada ruta llama a una función de `posts/views.py`, que renderiza su template HTML. En la preentrega 8, Inicio presentaba texto de bienvenida; la lista dinámica de publicaciones se agregó en la preentrega 9. Los posts de la versión por consola siguen en `posts.json`.

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
python manage.py migrate
python manage.py runserver
```

Abrí `http://127.0.0.1:8000/` en el navegador. Para detener el servidor, presioná `Ctrl+C` en la terminal.

En desarrollo, Django usa una clave local de ejemplo. Para reemplazarla, definí la variable de entorno `DJANGO_SECRET_KEY` antes de iniciar el servidor. Nunca uses la clave de ejemplo en un despliegue público.

### Pruebas

Las pruebas del blog por consola usan archivos temporales para comprobar la búsqueda, el filtrado y el guardado/carga de JSON. Las pruebas web usan una base de datos y carpetas de imágenes temporales para comprobar las páginas públicas y las operaciones de Gestión; no modifican los posts de tu base local.

```shell
python -m unittest discover -s tests
python manage.py test posts
```

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
