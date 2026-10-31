from django.http import Http404
from django.shortcuts import render
from blog.datos import posts

def inicio(request):
    busqueda = request.GET.get("q", "").strip()
    tag_buscado = request.GET.get("tag", "").strip()
    tag_buscado_limpio = tag_buscado.lower().replace(" ", "").lstrip("#")

    posts_filtrados = []

    for post in posts:
        coincide_titulo = busqueda.lower() in post["titulo"].lower()

        coincide_tag = not tag_buscado_limpio or any(
            tag_buscado_limpio in tag.lower().replace(" ", "").lstrip("#")
            for tag in post.get("tags", [])
        )

        if coincide_titulo and coincide_tag:
            posts_filtrados.append(post)

    return render(
        request,
        "web/inicio.html",
        {
            "posts": posts_filtrados,
            "busqueda": busqueda,
            "tag_buscado": tag_buscado,
        },
    )

def detalle_post(request, post_id):
    post_encontrado = None

    for post in posts:
        if post["id"] == post_id:
            post_encontrado = post
            break

    if post_encontrado is None:
        raise Http404("Blog no encontrado.")

    return render(request, "web/detalle.html", {"post": post_encontrado})