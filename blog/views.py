from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def hola(request):
    return HttpResponse("Hola Django!")