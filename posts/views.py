from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm
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


# Muestra todos los posts para gestionarlos, incluidos los borradores.
def gestion_posts(request):
    posts = Post.objects.order_by("-fecha_creacion")
    return render(request, "posts/gestion_posts.html", {"posts": posts})


# Valida los datos y la imagen recibidos; luego muestra el nuevo post en Gestión.
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("posts:gestion_posts")
    else:
        form = PostForm()

    return render(
        request,
        "posts/post_form.html",
        {"form": form, "titulo_pagina": "Crear publicación"},
    )


# Carga un post en el formulario y guarda los cambios sobre ese mismo registro.
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:gestion_posts")
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "posts/post_form.html",
        {"form": form, "titulo_pagina": "Editar publicación"},
    )


# Muestra la confirmación con GET y elimina el registro solo al recibir POST.
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        post.delete()
        return redirect("posts:gestion_posts")

    return render(request, "posts/post_confirmacion_delete.html", {"post": post})
