from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError

from apps.usuarios.models import Usuario


@login_required
def perfil(request):
    """CDU-004: Visualizar conta (perfil)"""
    usuario = request.user
    
    # Dados do usuário
    turmas = usuario.turmas.all().count()
    calendarios = usuario.calendarios.filter(turma=None).count()
    
    context = {
        'usuario': usuario,
        'total_turmas': turmas,
        'total_calendarios': calendarios,
        'turmas': usuario.turmas.all()[:5],  # Últimas 5 turmas
        'calendarios': usuario.calendarios.filter(turma=None)[:5]  # Últimos 5 calendários
    }
    return render(request, 'meu_perfil.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def editar_perfil(request):
    """CDU-005: Atualizar conta (perfil)"""
    usuario = request.user
    
    if request.method == 'GET':
        return render(request, 'usuarios/editar_perfil.html', {
            'usuario': usuario
        })
    
    # POST - Atualizar perfil
    try:
        nome_completo = request.POST.get('nome_completo', '').strip()
        
        if not nome_completo:
            raise ValidationError('Nome completo é obrigatório.')
        
        if len(nome_completo) < 3:
            raise ValidationError('Nome completo deve ter pelo menos 3 caracteres.')
        
        usuario.nome_completo = nome_completo
        usuario.save()
        
        return redirect('perfil')
    
    except ValidationError as e:
        return render(request, 'usuarios/editar_perfil.html', {
            'usuario': usuario,
            'error': str(e)
        })


@login_required
@require_http_methods(["GET", "POST"])
def alterar_senha(request):
    """CDU-006: Alterar senha"""
    usuario = request.user
    
    if request.method == 'GET':
        return render(request, 'usuarios/alterar_senha.html')
    
    # POST - Alterar senha
    try:
        senha_atual = request.POST.get('senha_atual', '')
        nova_senha = request.POST.get('nova_senha', '')
        confirmar_senha = request.POST.get('confirmar_senha', '')
        
        # Validar senha atual
        if not usuario.check_password(senha_atual):
            raise ValidationError('Senha atual incorreta.')
        
        # Validar senhas
        if not nova_senha:
            raise ValidationError('Nova senha é obrigatória.')
        
        if len(nova_senha) < 6:
            raise ValidationError('Nova senha deve ter pelo menos 6 caracteres.')
        
        if nova_senha != confirmar_senha:
            raise ValidationError('As senhas não conferem.')
        
        if senha_atual == nova_senha:
            raise ValidationError('Nova senha deve ser diferente da anterior.')
        
        # Alterar senha
        usuario.set_password(nova_senha)
        usuario.save()
        
        return render(request, 'usuarios/alterar_senha.html', {
            'sucesso': 'Senha alterada com sucesso!'
        })
    
    except ValidationError as e:
        return render(request, 'usuarios/alterar_senha.html', {
            'error': str(e)
        })
