from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

# vista de inicio de sesion
class Acceso(LoginView):
    template_name = 'autenticacion/acceso.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

# clase para cerrar la sesion actual
class CerrarSesion(LogoutView):
    next_page = 'home'

# vista para registrar una nueva cuenta de usuario
class RegistrarUsuario(FormView):
    template_name = 'autenticacion/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        usurio = form.save()
        if usurio is not None:
            login(self.request, usurio)
        return super(RegistrarUsuario, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegistrarUsuario, self).get(*args, **kwargs)
    

