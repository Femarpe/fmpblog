from urllib import request

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

# Create your views here.
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