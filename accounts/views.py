from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import PerfilForm, RegistroForm
from .models import Perfil

# Crea el usuario y su perfil; después inicia su sesión.
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Perfil.objects.create(user=usuario)
            login(request, usuario)
            return redirect("posts:inicio")
    else:
        form = RegistroForm()

    return render(request, "accounts/registro.html", {"form": form})


# Muestra el perfil de la persona que inició sesión.
@login_required
def perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, "accounts/perfil.html", {"perfil": perfil_usuario})


# Guarda la biografía y el avatar del usuario autenticado.
@login_required
def editar_perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect("accounts:perfil")
    else:
        form = PerfilForm(instance=perfil_usuario)

    return render(request, "accounts/editar_perfil.html", {"form": form})
