from django.urls import path
from .views import (
    LoginView, 
    RegistroView,
    UsuarioListView,
    UsuarioDetailView,
    UsuarioUpdateView,
    UsuarioDeleteView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('', UsuarioListView.as_view(), name='usuario-list'),
    path('usuarios/<int:pk>/', UsuarioDetailView.as_view(), name='usuario-detail'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario-update'),
    path('usuarios/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='usuario-delete'),
]