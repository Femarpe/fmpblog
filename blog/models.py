from django.db import models
#creamos una clase que extiende de models
class Categoria(models.Model):
    #definimos el tipo y sus atributos
    # NO tenemos clave primaria - PK, la asigna django
    # CharField (input text), TextField (textarea)...
    # atributos: long max 100, no permite nulos, campo único
    # verbose_name: nombre de la etiqueta del formulario
    nombre = models.CharField(max_length=100, null=False, unique=True, verbose_name='Nombre')
    # str nos permite devolver la información de la clase en forma de cadena
    def __str__(self):
        #si hacemos un print, en vez de mostrar el objeto, nos mostrará el nombre de la Categoría
        return self.nombre # return "Categoría con id %d y nombre %s" % (self.id, self.nombre)
    # Meta nos permite cambiar el comportamiento de las migraciones en BBDD
    # auth_user se llama así porque pertenece a la aplicación auth y el modelo user
    # por esa regla, categorías se llamaría por defecto: blog_Categoria
    # con Meta cambiamos este comportamiento
    class Meta:
        db_table = 'categories'
        verbose_name = 'Categoría' #nombre administración
        verbose_name_plural = 'Categorías'
        ordering = ['id'] #ordenación ascendente -- [-id] ordenación descendente