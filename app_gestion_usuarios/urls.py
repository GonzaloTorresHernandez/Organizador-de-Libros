from django.urls import path
from . import views
from .views import Acceso, CerrarSesion, RegistrarUsuario
from django.contrib.auth.views import LogoutView

urlpatterns = [
                path('Iniciar-Sesion', Acceso.as_view(), name='acceso-usuario'),
                path('Cerrar-Sesion', CerrarSesion.as_view(), name='cerrar-sesion'),
                path('Registrar-Usuario', RegistrarUsuario.as_view(), name='registrar-usuario')
               ]