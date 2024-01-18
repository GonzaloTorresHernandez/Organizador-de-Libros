from django.urls import path
from .views import Home_Vista, DetalleLibro, CrearComentario, ListaLibroAutor
from .views import ListaLibros,  CrearLibro, EditarLibro, EliminarLibro
from .views import ListaAutores, CrearAutor, EditarAutor, EliminarAutor
from .views import ListaGeneros, CrearGenero, EditarGenero, EliminarGenero
from . import views

urlpatterns = [path("", Home_Vista.as_view(), name='home'),
               path('Detalle-Libro/<int:id_libro>', DetalleLibro.as_view(), name='detalle-libro'),
               path('Comentar-Libro/<int:id_libro>', CrearComentario.as_view(), name='comentario-libro'),
               path('Libro-Autor/<int:id_autor>', ListaLibroAutor.as_view(), name='libro-autor'),

               path('libro-pdf', views.libro_pdf, name='libro-pdf'),

               path('Lista-Libro', ListaLibros.as_view(), name='lista-libro'),
               path('Agregar-Libro', CrearLibro.as_view(), name='crear-libro'),
               path('Editar-Libro/<int:pk>', EditarLibro.as_view(), name='editar-libro'),
               path('Eliminar-Libro/<libro_id>', views.eliminar_libro, name='eliminar-libro'),

               path('Lista-Autor', ListaAutores.as_view(), name='lista-autor'),
               path('Agregar-Autor', CrearAutor.as_view(), name='crear-autor'),
               path('Editar-Autor/<int:pk>', EditarAutor.as_view(), name='editar-autor'),
               path('Eliminar-Autor/<autor_id>', views.eliminar_autor, name='eliminar-autor'),

               path('Lista-Genero', ListaGeneros.as_view(), name='lista-genero'),
               path('Agregar-Genero', CrearGenero.as_view(), name='crear-genero'),
               path('Editar-Genero/<int:pk>', EditarGenero.as_view(), name='editar-genero'),
               path('Eliminar-Genero/<genero_id>', views.eliminar_genero, name='eliminar-genero'),]

#path('Eliminar-Genero/<int:pk>', EliminarGenero.as_view(), name='eliminar-genero'),
#path('Eliminar-Autor/<int:pk>', EliminarAutor.as_view(), name='eliminar-autor'),
#path('Eliminar-Libro/<int:pk>', EliminarLibro.as_view(), name='eliminar-libro'),