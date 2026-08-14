from django.urls import path
from . import views

app_name = 'calendarios'

urlpatterns = [
    # CDU-007-011: CRUD Calendário
    path('criar/', views.criar_calendario, name='criar_calendario'),
    path('<int:id>/', views.calendario_detalhe, name='calendario_detalhe'),
    path('<int:id>/editar/', views.atualizar_calendario, name='atualizar_calendario'),
    path('<int:id>/deletar/', views.deletar_calendario, name='deletar_calendario'),
    
    # Gerenciar membros
    path('<int:id>/membros/adicionar/', views.adicionar_membro_calendario, name='adicionar_membro'),
    path('<int:id>/membros/<int:membro_id>/remover/', views.remover_membro_calendario, name='remover_membro'),
    path('<int:id>/membros/<int:membro_id>/tornar-admin/', views.tornar_admin_calendario, name='tornar_admin'),
    path('<int:id>/membros/<int:membro_id>/remover-admin/', views.remover_admin_calendario, name='remover_admin'),
]
