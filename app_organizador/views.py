from typing import Any

from django.db.models.query import QuerySet
from .models import Libro, Autor, Genero, Comentario
from django.views.generic import TemplateView
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#pdf
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


#Vista HOME
class Home_Vista(TemplateView):
    template_name = 'home.html'

    # metodo para proporcionar los modelos a la plantilla
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['libros'] = Libro.objects.all()
        context['autores'] = Autor.objects.all()
        return  context

# Vista para Detalle de Libro
class DetalleLibro(TemplateView):
    template_name = 'libro/detalle_libro.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        #id de libro por la ruta
        id_libro = self.kwargs.get('id_libro')
        context['libro'] = Libro.objects.all()
        context['libro'] = context['libro'].filter(id=id_libro)
        context['comentarios'] = Comentario.objects.all().filter(libro=id_libro)
        return context

# Clase para definir el formulario de Libro
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto_comentario']
        labels = {'texto_comentario': 'Comentario',
                  }
        widgets = {
            'texto_comentario': forms.Textarea(attrs={'class': 'form-control',
                                              'placeholder': 'Contenido del Comentario...'})}
        error_messages = {
            'texto_comentario': {
                'required': 'Este campo es Obligatorio'
            }
        }

# Vista para agregar un comentario
class CrearComentario(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    success_url = reverse_lazy('home')
    template_name = 'libro/comentario_libro.html'
    login_url = reverse_lazy('acceso-usuario')

    # definir creador con el usuario actual automáticamente
    def form_valid(self, form):
        libro_id = self.kwargs.get('id_libro')
        form.instance.libro = get_object_or_404(Libro, pk=libro_id)
        form.instance.usuario = self.request.user
        return super(CrearComentario, self).form_valid(form)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        #id de libro por la ruta
        id_libro = self.kwargs.get('id_libro')
        context['libro'] = Libro.objects.all().filter(id=id_libro)
        return context

#Vista de Lista de libro de 1 Autor
class ListaLibroAutor(ListView):
    model = Libro
    template_name = 'libro/lista_libro_autor.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        id_autor = self.kwargs.get('id_autor')
        context['libros'] = Libro.objects.all().filter(autores = id_autor)
        return context

# Vista para ver Libros.
class ListaLibros(LoginRequiredMixin, View):
    model = Libro
    template_name = 'libro/read_libro.html'
    context_object_name = 'libros'
    login_url = reverse_lazy('acceso-usuario')

    #crear paginacion
    paginate_by = 2

    # Fitros y paginacion
    def get(self, request, *args, **kwargs):
        queryset = Libro.objects.filter(usuario=self.request.user)
        valor_buscado = self.request.GET.get('input-buscar') or ''
        filtro_buscado = self.request.GET.get('filtro-buscar')

        if valor_buscado:
            if filtro_buscado == 'titulo' or filtro_buscado == '':
                queryset = queryset.filter(titulo__icontains=valor_buscado)
            elif filtro_buscado == 'autor':
                queryset = queryset.filter(autores__nombre__icontains=valor_buscado)
            elif filtro_buscado == 'genero':
                queryset = queryset.filter(generos__nombre__icontains=valor_buscado)

        paginator = Paginator(queryset, self.paginate_by)
        page = request.GET.get('pagina')

        try:
            libros = paginator.page(page)
        except PageNotAnInteger:
            libros = paginator.page(1)
        except EmptyPage:
            libros = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'libros': libros})
        
# Clase para definir el formulario de Libro
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'descripcion', 'anio_publicacion', 'autores', 'generos']
        labels = {'titulo': 'Titulo',
                  'descripcion': 'Descripcion',
                  'anio_publicacion': 'Año de Publicacion',
                  'autores': 'Autor/@s',
                  'generos': 'Genero/s',}
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Titulo del libro'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 
                                                  'placeholder': 'Una breve Descripcion...'}),
            'anio_publicacion': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': '0000'}),
            'autores': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'generos': forms.SelectMultiple(attrs={'class': 'form-select'})
        }
        error_messages = {
            'titulo': {
                'required': 'Este campo es Obligatorio'
            },
            'autores': {
                'required': 'Debes elegir al autor/es del libro'
            },
            'generos': {
                'required': 'Debes elegir el genero/s del libro'
            },
            'anio_publicacion': {
                'invalid': 'El valor ingresado debe ser numerico.'
            }
        }

# Vista para Agregar un Libro
class CrearLibro(LoginRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    success_url = reverse_lazy('lista-libro')
    template_name = 'libro/create_libro.html'
    login_url = reverse_lazy('acceso-usuario')

    # definir creador con el usuario actual automáticamente
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearLibro, self).form_valid(form)
    
#Vista para Editar un libro:
class EditarLibro(LoginRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    success_url = reverse_lazy('lista-libro')
    template_name = 'libro/update_libro.html'
    login_url = reverse_lazy('acceso-usuario')

#Vista para Eliminar un libro:
class EliminarLibro(LoginRequiredMixin, DeleteView):
    model = Libro
    context_object_name = 'libro'
    success_url = reverse_lazy('lista-libro')
    template_name = 'libro/delete_libro.html'
    success_message = "El libro se elimino correctamente"
    login_url = reverse_lazy('acceso-usuario')

#Vista para Ver Autores
class ListaAutores(LoginRequiredMixin, ListView):
    model = Autor
    template_name = 'autor/read_autor.html'
    context_object_name = 'autores'
    login_url = reverse_lazy('acceso-usuario')

# Clase para definir el formulario de Autor
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre']
        labels = {'nombre': 'Nombre',}
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Nombre del Autor'})}
        error_messages = {
            'nombre': {
                'required': 'Este campo es Obligatorio'
            }
        }

# Vista para Agregar un Autor
class CrearAutor(LoginRequiredMixin, CreateView):
    model = Autor
    form_class = AutorForm
    success_url = reverse_lazy('lista-autor')
    template_name = 'autor/create_autor.html'
    login_url = reverse_lazy('acceso-usuario')
   
#Vista para Editar un autor:
class EditarAutor(LoginRequiredMixin, UpdateView):
    model = Autor
    form_class = AutorForm
    success_url = reverse_lazy('lista-autor')
    template_name = 'autor/update_autor.html'
    login_url = reverse_lazy('acceso-usuario')

#Vista para Eliminar un autor:
class EliminarAutor(LoginRequiredMixin, DeleteView):
    model = Autor
    context_object_name = 'autor'
    success_url = reverse_lazy('lista-autor')
    template_name = 'autor/delete_autor.html'
    success_message = "El autor se elimino correctamente"
    login_url = reverse_lazy('acceso-usuario')

#Vista para Ver Autores
class ListaGeneros(LoginRequiredMixin, ListView):
    model = Genero
    template_name = 'genero/read_genero.html'
    context_object_name = 'generos'
    login_url = reverse_lazy('acceso-usuario')

# Clase para definir el formulario de Genero
class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nombre']
        labels = {'nombre': 'Nombre',}
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Nombre del Genero'})}
        error_messages = {
            'nombre': {
                'required': 'Este campo es Obligatorio'
            }
        }

# Vista para Agregar un Genero
class CrearGenero(LoginRequiredMixin, CreateView):
    model = Genero
    form_class = GeneroForm
    success_url = reverse_lazy('lista-genero')
    template_name = 'genero/create_genero.html'
    login_url = reverse_lazy('acceso-usuario')
   
#Vista para Editar un Genero:
class EditarGenero(LoginRequiredMixin, UpdateView):
    model = Genero
    form_class = GeneroForm
    success_url = reverse_lazy('lista-genero')
    template_name = 'genero/update_genero.html'
    login_url = reverse_lazy('acceso-usuario')

#Vista para Eliminar un Genero:
class EliminarGenero(LoginRequiredMixin, DeleteView):
    model = Genero
    context_object_name = 'genero'
    success_url = reverse_lazy('lista-genero')
    template_name = 'genero/delete_genero.html'
    success_message = "El genero se elimino correctamente"  
    login_url = reverse_lazy('acceso-usuario')  


#Funcion para eliminar Genero
def eliminar_genero(request, genero_id):
    genero = Genero.objects.get(pk=genero_id)
    genero.delete()
    return redirect('lista-genero')

#Funcion para eliminar Autor
def eliminar_autor(request, autor_id):
    autor = Autor.objects.get(pk=autor_id)
    autor.delete()
    return redirect('lista-autor')

#Funcion para eliminar Libro
def eliminar_libro(request, libro_id):
    libro = Libro.objects.get(pk=libro_id)
    libro.delete()
    return redirect('lista-libro')


#funcion para descarga un pdf
def libro_pdf(request):
    buf = io.BytesIO() #buffer
    can = canvas.Canvas(buf, pagesize=letter, bottomup=0) #canvas

    # objeto que contendra el texto
    texto = can.beginText()
    texto.setTextOrigin(inch, inch)
    texto.setFont('Helvetica', 14)

    #designar el modelo
    libros = Libro.objects.all()

    #lista vacia
    lineas = []

    #cargar lista
    for libro in libros:
        
        lineas.append(libro.titulo)
        lineas.append(libro.descripcion)
        lineas.append(str(libro.anio_publicacion))

        # autores y generos
        autores = [autor.nombre for autor in libro.autores.all()]
        generos = [genero.nombre for genero in libro.generos.all()]
        lineas.append(', '.join(autores))
        lineas.append(', '.join(generos))

        lineas.append(" ")
    #cargar lineas al archivo
    for linea in lineas:
        texto.textLine(linea)

    #terminar subida
    can.drawText(texto)
    can.showPage()
    can.save()
    buf.seek(0)

    #retorar algo
    return FileResponse(buf, as_attachment=True, filename='libros.pdf')
        




