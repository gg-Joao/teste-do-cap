from django.urls import path
from .views import (
    criar_evento,
    evento_detalhe, 
    atualizar_evento,
    deletar_evento,
    teste_modal
)

app_name = 'eventos'

urlpatterns = [
    path('criar/', criar_evento, name='criar_evento'),
    path('<int:pk>/', evento_detalhe, name='evento_detalhe'),
    path('<int:pk>/editar/', atualizar_evento, name='atualizar_evento'),
    path('<int:pk>/deletar/', deletar_evento, name='deletar_evento'),
    path('teste-modal/', teste_modal, name='teste_modal'),
]
