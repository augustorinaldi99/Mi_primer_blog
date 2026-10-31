from django.urls import include, path
from . import views

app_name = "web"

urlpatterns = [
    path("", views.inicio, name= "inicio"),
    path("posts/<int:post_id>/", views.detalle_post, name="detalle_post"),
]