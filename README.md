# Mi primer blog

Blog web desarrollado con Django para publicar entradas sobre películas y series de superhéroes. Las preentregas anteriores permanecen en el historial de Git; la versión actual usa modelos y una base SQLite. Ya no carga publicaciones desde archivos JSON.

**Autor:** Augusto Rinaldi.

## Tecnologías

- Python (probado con 3.14.7) y Django 6.1.2.
- SQLite para publicaciones, etiquetas, usuarios y perfiles.
- Pillow para procesar las imágenes subidas.
- HTML y CSS para las páginas; JavaScript para habilitar la edición de tags en el administrador.

Las dependencias y sus versiones están en `requirements.txt`.

## Funcionalidades

- Cualquier visitante puede leer publicaciones con estado `publicado`, buscar por título o tag y abrir un tag para ver las publicaciones que lo comparten. La búsqueda ignora mayúsculas y tildes, pero distingue `ñ` de `n`. Los resultados se muestran de a tres por página.
- Los usuarios pueden registrarse, iniciar y cerrar sesión, y editar su biografía y avatar.
- Cada cuenta puede crear publicaciones y gestionar **solo las propias**: editar, eliminar y ver la vista previa privada de borradores y archivados. Las imágenes y los tags son opcionales.
- El nombre visible del autor se toma de la cuenta al crear el post. La relación `creado_por` identifica al dueño para controlar el acceso.
- Los tags conservan el orden indicado al editarlos desde Gestión o Administración.
- Las cuentas con permiso de personal pueden entrar a `/admin/` para administrar el sitio.

## Estructura

- `blog_project/`: configuración general y rutas del proyecto.
- `posts/`: modelos, formularios, páginas, CSS, JavaScript, migraciones y pruebas de publicaciones.
- `accounts/`: registro, acceso, perfiles, migraciones y pruebas de usuarios.
- `manage.py`: comandos de Django.

## Instalación y ejecución

Cloná el repositorio y entrá en la carpeta del proyecto:

```bash
git clone https://github.com/augustorinaldi99/Mi_primer_blog.git
cd Mi_primer_blog
python -m venv .venv
```

Activá el entorno virtual según la terminal:

```bash
# Git Bash en Windows
source .venv/Scripts/activate

# Linux o macOS
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Instalá las dependencias, prepará la base de datos e iniciá el servidor:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrí `http://127.0.0.1:8000/`. Para detener el servidor, presioná `Ctrl+C` en la terminal.

### Primer uso en una instalación nueva

El repositorio no incluye `db.sqlite3` ni `media/`. Una instalación nueva comienza sin usuarios, publicaciones ni imágenes. Registrá una cuenta desde **Crear cuenta** (`/accounts/registro/`); la sesión se inicia automáticamente. Desde **Gestión** (`/gestion/`) podés crear un post. Si elegís el estado `publicado`, aparecerá en Inicio; un borrador o archivado solo estará disponible para su dueño desde Gestión y Vista previa.

Podés subir una imagen y escribir tags separados por comas, cada uno comenzando con `#`. El formulario muestra los tags en el orden guardado. Para tener más de una página en Inicio, creá al menos cuatro publicaciones **publicadas**.

El buscador admite coincidencias parciales por título o tag: por ejemplo, `que` encuentra `Qué`, y `heroe cosmico` puede encontrar el tag `#HéroeCósmico`. Al pasar de página se conserva el término buscado. Al hacer clic en un tag se muestran solo las publicaciones publicadas que tienen ese tag exacto.

Para usar el panel administrativo, creá una cuenta administradora con `python manage.py createsuperuser` y entrá a `http://127.0.0.1:8000/admin/`. Al editar tags allí, marcá **Modificar tags** antes de cambiar el texto.

Las imágenes se guardan en `media/posts/` y `media/avatares/`; SQLite guarda sus rutas. Tanto `media/` como `db.sqlite3` están excluidos de Git, por lo que los datos locales no se incluyen al clonar el repositorio.

### Clave y uso local

`settings.py` admite `DJANGO_SECRET_KEY` como variable de entorno y usa una clave de desarrollo si no se define. `.env.example` muestra el nombre de la variable, pero el proyecto no lee archivos `.env` automáticamente: definí la variable en la terminal antes de iniciar Django si querés reemplazarla. Nunca subas una clave privada real al repositorio.

La configuración actual es para desarrollo local (`DEBUG=True`). Antes de publicar el sitio en internet habrá que configurar una clave privada, desactivar `DEBUG`, definir `ALLOWED_HOSTS` y revisar el despliegue.

## Comprobaciones

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Las pruebas usan una base de datos y carpetas de imágenes temporales; no modifican los posts de la base local.
La suite actual contiene 24 pruebas que cubren acceso, edición, imágenes, tags, búsqueda y paginación.
