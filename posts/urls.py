from django.urls import path

from . import views

app_name = "posts"

# Relaciona cada dirección del blog con la vista que prepara su página.
urlpatterns = [
    path("", views.lista_posts, name="inicio"),
    path("acerca/", views.acerca, name="acerca"),
    path("posts/<int:post_id>/", views.detalle_post, name="detalle_post"),
    path("gestion/", views.gestion_posts, name="gestion_posts"),
    path("posts/crear/", views.crear_post, name="crear_post"),
    path("posts/<int:post_id>/editar/", views.editar_post, name="editar_post"),
    path("posts/<int:post_id>/eliminar/", views.eliminar_post, name="eliminar_post"),
    path("tags/<int:tag_id>/", views.posts_por_tag, name="posts_por_tag"),
    path("posts/<int:post_id>/vista-previa/", views.vista_previa_post, name="vista_previa_post"),
]
