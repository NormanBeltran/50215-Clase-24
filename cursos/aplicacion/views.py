from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import *
from .forms import * 


from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Copyright Norman Beltran

def home(request):
    return render(request, "aplicacion/index.html") 


@login_required
def entregables(request):
    return render(request, "aplicacion/entregables.html") 

#________________________________________ Adicionales
def acerca(request):
    return render(request, "aplicacion/acerca.html") 

#________________________________________ Cursos
@login_required
def cursos(request):
    contexto = {'cursos': Curso.objects.all().order_by("id")}
    return render(request, "aplicacion/cursos.html", contexto) 

@login_required
def cursoCreate(request):
    # __ Si ingresa en el if es la 2da o enesima vez que llega el formulario
    if request.method == "POST":
        miForm = CursoForm(request.POST)
        if miForm.is_valid():
            curso_nombre = miForm.cleaned_data.get("nombre")
            curso_comision = miForm.cleaned_data.get("comision")
            curso = Curso(nombre=curso_nombre, comision=curso_comision)
            curso.save()
            return redirect(reverse_lazy('cursos'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = CursoForm()

    return render(request, "aplicacion/cursoForm.html", {"form": miForm} )

@login_required
def cursoUpdate(request, id_curso):
    curso = Curso.objects.get(id=id_curso)
    if request.method == "POST":
        miForm = CursoForm(request.POST)
        if miForm.is_valid():
            curso.nombre = miForm.cleaned_data.get("nombre")
            curso.comision = miForm.cleaned_data.get("comision")
            curso.save()
            return redirect(reverse_lazy('cursos'))
    else:
        miForm = CursoForm(initial={'nombre': curso.nombre, 'comision': curso.comision})

    return render(request, "aplicacion/cursoForm.html", {"form": miForm} )

@login_required
def cursoDelete(request, id_curso):
    curso = Curso.objects.get(id=id_curso)
    curso.delete()
    return redirect(reverse_lazy('cursos'))

#________________________________________ Profesores
@login_required
def profesores(request):
    contexto = {'profesores': Profesor.objects.all().order_by("id")}
    return render(request, "aplicacion/profesores.html", contexto) 

@login_required
def profesorCreate(request):
    # __ Si ingresa en el if es la 2da o enesima vez que llega el formulario
    if request.method == "POST":
        miForm = ProfesorForm(request.POST)
        if miForm.is_valid():
            prof_nombre = miForm.cleaned_data.get("nombre")
            prof_apellido = miForm.cleaned_data.get("apellido")
            prof_email = miForm.cleaned_data.get("email")
            prof_profesion = miForm.cleaned_data.get("profesion")

            profesor = Profesor(nombre=prof_nombre, 
                             apellido=prof_apellido,
                             email=prof_email,
                             profesion=prof_profesion)
            profesor.save()
            return redirect(reverse_lazy('profesores'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = ProfesorForm()

    return render(request, "aplicacion/profesorForm.html", {"form": miForm} )

@login_required
def profesorUpdate(request, id_profesor):
    profesor = Profesor.objects.get(id=id_profesor)
    if request.method == "POST":
        miForm = ProfesorForm(request.POST)
        if miForm.is_valid():
            profesor.nombre = miForm.cleaned_data.get("nombre")
            profesor.apellido = miForm.cleaned_data.get("apellido")
            profesor.email = miForm.cleaned_data.get("email")
            profesor.profesion = miForm.cleaned_data.get("profesion")
            profesor.save()
            return redirect(reverse_lazy('profesores'))
    else:
        miForm = ProfesorForm(initial={'nombre': profesor.nombre, 
                                       'apellido': profesor.apellido,
                                       'email': profesor.email,
                                       'profesion': profesor.profesion,
                                       })

    return render(request, "aplicacion/profesorForm.html", {"form": miForm} )

@login_required
def profesorDelete(request, id_profesor):
    profesor = Profesor.objects.get(id=id_profesor)
    profesor.delete()
    return redirect(reverse_lazy('profesores'))

#________________________ Buscar
@login_required
def buscarCursos(request):
    return render(request, "aplicacion/buscar.html")

@login_required
def encontrarCursos(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        cursos = Curso.objects.filter(nombre__icontains=patron)
        contexto = {"cursos": cursos}
        return render(request, "aplicacion/cursos.html", contexto)
    

    contexto = {'cursos': Curso.objects.all()}
    return render(request, "aplicacion/cursos.html", contexto) 

#________________________ Estudiantes
class EstudianteList(LoginRequiredMixin, ListView):
    model = Estudiante

class EstudianteCreate(LoginRequiredMixin, CreateView):
    model = Estudiante
    fields = ["nombre", "apellido", "email"]
    success_url = reverse_lazy("estudiantes")

class EstudianteUpdate(LoginRequiredMixin, UpdateView):
    model = Estudiante
    fields = ["nombre", "apellido", "email"]
    success_url = reverse_lazy("estudiantes")

class EstudianteDelete(LoginRequiredMixin, DeleteView):
    model = Estudiante
    success_url = reverse_lazy("estudiantes")  

#________________________ Login, Logout, Authentication, Registration
def login_request(request):         
    if request.method == "POST":
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)

            #______ Avatar
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar

            #________________________________________________________

            return render(request, "aplicacion/index.html")
        else:
            return redirect(reverse_lazy('login'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = AuthenticationForm()

    return render(request, "aplicacion/login.html", {"form": miForm} )

def register(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)

        if miForm.is_valid():
            usuario = miForm.cleaned_data.get("username")
            miForm.save()
            return redirect(reverse_lazy('home'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = RegistroForm()

    return render(request, "aplicacion/registro.html", {"form": miForm} )  

#________________________ Edición de Perfil, Cambio Clave, Avatar

@login_required
def editProfile(request):
    usuario = request.user
    if request.method == "POST":
        miForm = UserEditForm(request.POST)
        if miForm.is_valid():
            user = User.objects.get(username=usuario)
            user.email = miForm.cleaned_data.get("email")
            user.first_name = miForm.cleaned_data.get("first_name")
            user.last_name = miForm.cleaned_data.get("last_name")
            user.save()
            return redirect(reverse_lazy('home'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = UserEditForm(instance=usuario)

    return render(request, "aplicacion/editarPerfil.html", {"form": miForm} )    
   
class CambiarClave(LoginRequiredMixin, PasswordChangeView):
    template_name = "aplicacion/cambiar_clave.html"
    success_url = reverse_lazy("home")

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        miForm = AvatarForm(request.POST, request.FILES)

        if miForm.is_valid():
            usuario = User.objects.get(username=request.user)
            #___ Borrar avatares viejos
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            #____________________________________________________
            avatar = Avatar(user=usuario,
                            imagen=miForm.cleaned_data["imagen"])
            avatar.save()
            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session["avatar"] = imagen
            
            return redirect(reverse_lazy('home'))
    else:
    # __ Si ingresa en el else es la primera vez 
        miForm = AvatarForm()

    return render(request, "aplicacion/agregarAvatar.html", {"form": miForm} )      