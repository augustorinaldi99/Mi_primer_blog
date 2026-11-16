from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .busqueda import normalizar_tildes
from .forms import PostForm
from .models import Post, Tag


# Muestra la página con información sobre el autor y el sitio.
def acerca(request):
    return render(request, "posts/acerca.html")


# Ordena los posts y devuelve tres por página junto con los números de navegación.
def paginar_posts(request, posts):
    posts = posts.order_by("-fecha_creacion", "-pk")
    posts = posts.prefetch_related("etiquetas_ordenadas__tag")

    paginador = Paginator(posts, 3)
    pagina = paginador.get_page(request.GET.get("page"))
    numeros = paginador.get_elided_page_range(
        pagina.number, on_each_side=1, on_ends=1
    )
    return pagina, numeros


# Muestra los posts publicados y permite buscarlos por título o tag.
def lista_posts(request):
    busqueda = request.GET.get("q", "").strip()
    posts = Post.objects.filter(estado="publicado")

    if busqueda:
        termino_tag = "".join(busqueda.lstrip("#").split())
        condiciones = Q(titulo_normalizado__contains=normalizar_tildes(busqueda))

        if termino_tag:
            condiciones |= Q(
                etiquetas_ordenadas__tag__nombre_normalizado__contains=(
                    normalizar_tildes(termino_tag)
                )
            )

        posts = posts.filter(condiciones).distinct()

    pagina, numeros = paginar_posts(request, posts)
    return render(
        request,
        "posts/lista_posts.html",
        {
            "posts": pagina,
            "pagina": pagina,
            "numeros_pagina": numeros,
            "busqueda": busqueda,
        },
    )


# Muestra los posts publicados que tienen el tag seleccionado.
def posts_por_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    posts = Post.objects.filter(
        estado="publicado",
        etiquetas_ordenadas__tag=tag,
    )

    pagina, numeros = paginar_posts(request, posts)
    return render(
        request,
        "posts/lista_posts.html",
        {
            "posts": pagina,
            "pagina": pagina,
            "numeros_pagina": numeros,
            "tag_actual": tag,
            "busqueda": "",
        },
    )


# Muestra un post publicado; otros estados y los ID inexistentes devuelven 404.
def detalle_post(request, post_id):
    post = get_object_or_404(
        Post.objects.prefetch_related("etiquetas_ordenadas__tag"),
        id=post_id,
        estado="publicado",
    )
    return render(request, "posts/detalle_post.html", {"post": post})


# Permite al dueño revisar un post sin hacerlo público.
@login_required
def vista_previa_post(request, post_id):
    post = get_object_or_404(
        Post.objects.prefetch_related("etiquetas_ordenadas__tag"),
        id=post_id,
    )

    if post.creado_por_id != request.user.id:
        return render(
            request,
            "posts/sin_permiso.html",
            {"accion": "ver"},
            status=403,
        )

    return render(
        request,
        "posts/detalle_post.html",
        {"post": post, "vista_previa": True},
    )


# Muestra los posts del usuario, incluidos los borradores.
@login_required
def gestion_posts(request):
    posts = Post.objects.filter(creado_por=request.user).order_by("-fecha_creacion")
    return render(request, "posts/gestion_posts.html", {"posts": posts})


# Valida los datos y la imagen recibidos; luego muestra el nuevo post en Gestión.
@login_required
def crear_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            nuevo_post = form.save(commit=False)
            nuevo_post.creado_por = request.user
            nuevo_post.autor = request.user.get_full_name() or request.user.get_username()
            nuevo_post.save()
            form.guardar_tags(nuevo_post)
            return redirect("posts:gestion_posts")
    else:
        form = PostForm()

    return render(
        request,
        "posts/post_form.html",
        {"form": form, "titulo_pagina": "Crear publicación"},
    )


# Carga un post en el formulario y guarda los cambios sobre ese mismo registro.
@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.creado_por_id != request.user.id:
        return render(
            request,
            "posts/sin_permiso.html",
            {"accion": "editar"},
            status=403,
        )

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            form.guardar_tags(post)
            return redirect("posts:gestion_posts")
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "posts/post_form.html",
        {"form": form, "titulo_pagina": "Editar publicación"},
    )


# Muestra la confirmación con GET y elimina el registro solo al recibir POST.
@login_required
def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.creado_por_id != request.user.id:
        return render(
            request,
            "posts/sin_permiso.html",
            {"accion": "eliminar"},
            status=403,
        )

    if request.method == "POST":
        post.delete()
        return redirect("posts:gestion_posts")

    return render(request, "posts/post_confirmacion_delete.html", {"post": post})
