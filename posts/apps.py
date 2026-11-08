from django.apps import AppConfig


# Configura la aplicación y el nombre que aparece en el administrador.
class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = "Blog"
