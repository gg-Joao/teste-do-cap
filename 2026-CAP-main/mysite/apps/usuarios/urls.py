from django.urls import path
from . import views

urlpatterns = [
    path('', views.perfil, name='perfil'),
    path('editar/', views.editar_perfil, name='editar_perfil'),
    path('senha/', views.alterar_senha, name='alterar_senha'),
]