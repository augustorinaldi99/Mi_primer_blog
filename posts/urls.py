from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.lista_posts, name="inicio"),
    path("acerca/", views.acerca, name="acerca"),
    path("posts/<int:post_id>/", views.detalle_post, name="detalle_post"),
]