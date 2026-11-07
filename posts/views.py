from django.shortcuts import render

# Muestra la pagina de inicio del blog
def inicio(request):
    return render(request, "posts/inicio.html")

# Muestra la pagina acerca del autor y del sitio
def acerca(request):
    return render(request, "posts/acerca.html")
