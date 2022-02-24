from urllib import request

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

# Create your views here.
from blog.forms import FormularioPost
from blog.models import Post


def index(request):
    #return HttpResponse("Hola, bienvenid@ al Blog!")
    return render(request, "blog.html")

def post(self, request):
    #pasamos los datos del formulario - POST - para que django los procese
    form = UserCreationForm(request.POST)
    #validamos el formulario
    if form.is_valid():
        #si es válido, crea un usuario en la tabla auth_user vinculada en el modelo
        usuario = form.save()
        #cleaned_data limpia valores y solo contiene los campos del formulario
        nombre = form.cleaned_data.get("username")
        #creamos una sesion flash cuando se da de alta un usuario
        #F o f formatea el mensaje de respuesta permitiendo introducir variable -- Antonio!
        messages.success(request, F"Bienvenid@ a nuestro blog {nombre}")
        #identificamos al usuario
        login(request, usuario)
        #una vez que ha iniciado sesion lo redirigimos al blog y sus entradas
        return redirect("blog") #hacemos cambio de las urls
    else:
        # msg recoge los mensajes de error
        for msg in form.error_messages:
            messages.error(request, form.error_messages[msg])#extraemos el mensaje de error
        #si hay errores nos quedaremos en el formulario de registro
        return render(request, "registro.html", {"form": form})


def crear_post(request):
    if request.method == "POST": #comprobamos la petición
        # este formulario también recibe archivos
        # para procesarlos se han de incluir
        form = FormularioPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)#no guardamos de manera persistente porque nos falta el usuario
            #extraemos el usuario autenticado
            post.autor_id = request.user.id
            post.save()#ahora sí que guardamos la información
            titulo = form.cleaned_data.get("titulo")
            messages.success(request, f"El post {titulo} se ha creado correctamente")
            return redirect("blog")
        else:#si el formulario no es válido recorremos todos los mensajes y los devolvemos
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
    form = FormularioPost()#aquí tendríamos el formulario
    return render(request, "crear_post.html", {"form": form})#y se lo pasamos a la vista crear_post.html

#además de la petición, tendremos que pasar el elemento a eliminar
@login_required(login_url='/accounts/acceder')
def eliminar_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id) # recogemos el id del post de la url
    except Post.DoesNotExist: # por si se accede a una url de un post que NO existe
        messages.error(request, "El post que quieres eliminar no existe.")
        return redirect("blog")

    # si no se origina la excepción, el post existe;
    # por lo que se habrá de comprobar que el post que se quiere eliminar
    # es del usuario que hace la petición
    if post.autor != request.user:
        messages.error(request, "No eres el autor de este post.")
        return redirect("blog")

    # Existe el post y es el autor: eliminamos
    post.delete()
    messages.success(request, F"El post {post.titulo} ha sido eliminado!")
    return redirect("blog")