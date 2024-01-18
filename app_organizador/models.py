from django.db import models
from django.contrib.auth.models import User

"""
Tabla de Libros:

Columnas:
ID (identificador único)
Titulo
Descripcion
Año_Publicacion

Tabla de Autores:

Columnas:
ID_Autor (identificador único)
Nombre_Autor

Tabla de Géneros:

Columnas:
ID_Genero (identificador único)
Nombre_Genero

Tabla de Relación Libro-Autor:

Columnas:
ID_Libro_Autor (identificador único)
ID_Libro (clave foránea referenciando la tabla de Libros)
ID_Autor (clave foránea referenciando la tabla de Autores)

Tabla de Relación Libro-Género:

Columnas:
ID_Libro_Genero (identificador único)
ID_Libro (clave foránea referenciando la tabla de Libros)
ID_Genero (clave foránea referenciando la tabla de Géneros)
"""

# Create your models here.
class Genero(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    usuario = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True,
                                    blank=True)
    anio_publicacion = models.IntegerField(null=True,
                                        blank=True)
    autores = models.ManyToManyField(Autor)
    generos = models.ManyToManyField(Genero)

    def __str__(self):
        return self.titulo
    

class Comentario(models.Model):
    usuario = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    texto_comentario = models.TextField(null=False,
                                  blank=False)
    libro = models.ForeignKey(Libro, 
                              on_delete = models.CASCADE,
                              null=False,
                              blank = False)
    def __str__(self):
        return self.texto_comentario
