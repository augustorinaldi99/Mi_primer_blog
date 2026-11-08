from django.shortcuts import get_object_or_404, render
from .models import Post

# Conserva la vista de bienvenida de la etapa anterior; la ruta / usa lista_posts.
def inicio(request):
    return render(request, "posts/inicio.html")

# Muestra la página con información sobre el autor y el sitio.
def acerca(request):
    return render(request, "posts/acerca.html")

# Muestra solo los posts publicados, del más reciente al más antiguo.
def lista_posts(request):
    posts = Post.objects.filter(estado="publicado").order_by("-fecha_creacion")
    return render(request, "posts/lista_posts.html", {"posts": posts})
# Muestra un post publicado; otros estados y los ID inexistentes devuelven 404.
def detalle_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, estado="publicado")
    return render(request, "posts/detalle_post.html", {"post": post})
