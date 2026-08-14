from django.urls import path
from . import views

app_name = 'turmas'

urlpatterns = [
    # CDU-017-020: CRUD Turma
    path('criar/', views.criar_turma, name='criar_turma'),
    path('<int:id>/', views.turma_detalhe, name='turma_detalhe'),
    path('<int:id>/editar/', views.atualizar_turma, name='atualizar_turma'),
    path('<int:id>/deletar/', views.deletar_turma, name='deletar_turma'),
    
    # CDU-023-028: Gerenciar membros
    path('<int:id>/membros/adicionar/', views.adicionar_membro_turma, name='adicionar_membro'),
    path('<int:id>/membros/<int:membro_id>/remover/', views.remover_membro_turma, name='remover_membro'),
    path('<int:id>/membros/<int:membro_id>/tornar-admin/', views.tornar_admin_turma, name='tornar_admin'),
    path('<int:id>/membros/<int:membro_id>/remover-admin/', views.remover_admin_turma, name='remover_admin'),
    path('<int:id>/sair/', views.sair_turma, name='sair_turma'),
    path('<int:id>/membros/listar/', views.listar_membros_turma, name='listar_membros'),
]
