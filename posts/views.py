from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404, render

# Muestra la pagina de inicio del blog
def inicio(request):
    return render(request, "posts/inicio.html")

# Muestra la pagina acerca del autor y del sitio
def acerca(request):
    return render(request, "posts/acerca.html")

# Muestra la lista de Posts creados
def lista_posts(request):
    posts = Post.objects.filter(estado="publicado").order_by("-fecha_creacion")
    return render(request, "posts/lista_posts.html", {"posts": posts})

def detalle_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, estado="publicado")
    return render(request, "posts/detalle_post.html", {"post": post})