from django.urls import path
from . import views

app_name = "posts"

# Relaciona cada dirección del blog con la vista que prepara su página.
urlpatterns = [
    path("", views.lista_posts, name="inicio"),
    path("acerca/", views.acerca, name="acerca"),
    path("posts/<int:post_id>/", views.detalle_post, name="detalle_post"),
]
