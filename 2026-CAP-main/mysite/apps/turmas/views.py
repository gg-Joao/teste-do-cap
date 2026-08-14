from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.turmas.models import Turma, MembroDeTurma
from apps.usuarios.models import Usuario


def _usuario_eh_admin_turma(usuario, turma):
    """Verifica se usuário é admin da turma"""
    membro = MembroDeTurma.objects.filter(
        usuario=usuario,
        turma=turma
    ).first()
    return membro and membro.eh_admin


def _usuario_eh_membro_turma(usuario, turma):
    """Verifica se usuário é membro da turma"""
    return MembroDeTurma.objects.filter(
        usuario=usuario,
        turma=turma
    ).exists()


@login_required
def turma_detalhe(request, id):
    """CDU-018: Visualizar turma"""
    usuario = request.user
    turma = get_object_or_404(Turma, id=id)
    
    # Verificar se usuário é membro
    if not _usuario_eh_membro_turma(usuario, turma):
        return render(request, 'core/error.html', {
            'mensagem': 'Você não tem acesso a esta turma.'
        }, status=403)
    
    # Recuperar membros
    membros = MembroDeTurma.objects.filter(turma=turma).select_related('usuario')
    pode_gerenciar = _usuario_eh_admin_turma(usuario, turma)
    
    context = {
        'turma': turma,
        'membros': membros,
        'pode_gerenciar': pode_gerenciar,
        'eh_admin': pode_gerenciar,
        'membro_atual': MembroDeTurma.objects.get(usuario=usuario, turma=turma)
    }
    return render(request, 'turmas/turma.html', context)


@login_required
def criar_turma(request):
    """CDU-017: Criar turma"""
    usuario = request.user

    # Gerar nome único
    numero_turma = 1
    while True:
        if not usuario.turmas.filter(nome__icontains=f'Turma {numero_turma}'):
            break
        numero_turma += 1
    nome_turma = f'Turma {numero_turma}'

    # Criar turma
    turma = Turma.objects.create(
        nome=nome_turma,
        descricao=f'Bem vindo a {nome_turma}!'
    )

    # Adicionar criador como admin
    numero_paleta = usuario.paleta_menos_usada()
    MembroDeTurma.objects.create(
        usuario=usuario,
        turma=turma,
        eh_admin=True,
        numero_paleta=numero_paleta
    )

    return redirect('turmas:turma_detalhe', turma.id)


@login_required
@require_http_methods(["GET", "POST"])
def atualizar_turma(request, id):
    """CDU-019: Atualizar turma"""
    usuario = request.user
    turma = get_object_or_404(Turma, id=id)
    
    # Verificar permissões
    if not _usuario_eh_admin_turma(usuario, turma):
        return render(request, 'core/error.html', {
            'mensagem': 'Apenas administradores podem editar esta turma.'
        }, status=403)
    
    if request.method == 'GET':
        return render(request, 'turmas/editar_turma.html', {
            'turma': turma
        })
    
    # POST - Atualizar turma
    try:
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        
        if not nome:
            raise ValidationError('Nome da turma é obrigatório.')
        
        turma.nome = nome
        turma.descricao = descricao
        turma.save()
        
        return redirect('turmas:turma_detalhe', turma.id)
    
    except ValidationError as e:
        return render(request, 'turmas/editar_turma.html', {
            'turma': turma,
            'error': str(e)
        })


@login_required
@require_http_methods(["POST"])
def deletar_turma(request, id):
    """CDU-020: Deletar turma"""
    usuario = request.user
    turma = get_object_or_404(Turma, id=id)
    
    # Verificar permissões
    if not _usuario_eh_admin_turma(usuario, turma):
        return render(request, 'core/error.html', {
            'mensagem': 'Apenas administradores podem deletar esta turma.'
        }, status=403)
    
    turma.delete()
    return redirect('inicio')


@login_required
@require_http_methods(["POST"])
def adicionar_membro_turma(request, id):
    """CDU-023: Adicionar membro à turma"""
    usuario = request.user
    turma = get_object_or_404(Turma, id=id)
    
    # Verificar permissões
    if not _usuario_eh_admin_turma(usuario, turma):
        return JsonResponse({'erro': 'Sem permissão'}, status=403)
    
    try:
        email = request.POST.get('email', '').strip()
        
        if not email:
            return JsonResponse({'erro': 'Email é obrigatório'}, status=400)
        
        novo_usuario = get_object_or_404(Usuario, email=email)
        
        # Verificar se já é membro
        if _usuario_eh_membro_turma(novo_usuario, turma):
            return JsonResponse({
                'erro': 'Usuário já é membro desta turma'
            }, status=400)
        
        # Adicionar membro
        numero_paleta = novo_usuario.paleta_menos_usada()
        MembroDeTurma.objects.create(
            usuario=novo_usuario,
            turma=turma,
            eh_admin=False,
            numero_paleta=numero_paleta
        )
        
        return JsonResponse({
            'sucesso': True,
            'mensagem': f'{novo_usuario.email} foi adicionado à turma'
        })
    
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def remover_membro_turma(request, id, membro_id):
    """CDU-024: Remover membro da turma"""
    usuario = request.user
    turma = get_object_or_404(Turma, id=id)
    membro = get_object_or_404(MembroDeTurma, id=membro_id, turma=turma)
    
    # Verificar permissões
    if not _usuario_eh_admin_turma(usuario, turma):
        return JsonResponse({'erro': 'Sem permissão'}, status=403)
    
    # Não permitir remover a si mesmo se for o único admin
    if membro.usuario == usuario:
        admins = MembroDeTurma.objects.filter(turma=turma, eh_admin=True).count()
        if admins <= 1:
            return JsonResponse({
                'erro': 'Você é o único administrador. Não pode remover a si mesmo.'
            }, status=400)
    
    membro_removido = membro.usuario.email
    membro.delete()
    
    return JsonResponse({
        'sucesso': True,
        'mensagem': f'{membro_removido} foi removido da turma'
    })


@login_required
@require_http_methods(["POST"])
def tornar_admin_turma(request, id, membro_id):
    """CDU-025: Tornar membro admin"""
    usuario = request.user
    turma = get_object_or_404(Turma, id=id)
    membro = get_object_or_404(MembroDeTurma, id=membro_id, turma=turma)
    
    # Verificar permissões
    if not _usuario_eh_admin_turma(usuario, turma):
        return JsonResponse({'erro': 'Sem permissão'}, status=403)
    
    membro.eh_admin = True
    membro.save()
    
    return JsonResponse({
        'sucesso': True,
        'mensagem': f'{membro.usuario.email} agora é administrador'
    })


@login_required
@require_http_methods(["POST"])
def remover_admin_turma(request, id, membro_id):
    """CDU-026: Remover permissão de admin"""
    usuario = request.user
    turma = get_object_or_404(Turma, id=id)
    membro = get_object_or_404(MembroDeTurma, id=membro_id, turma=turma)
    
    # Verificar permissões
    if not _usuario_eh_admin_turma(usuario, turma):
        return JsonResponse({'erro': 'Sem permissão'}, status=403)
    
    # Não permitir remover a si mesmo se for o único admin
    if membro.usuario == usuario:
        admins = MembroDeTurma.objects.filter(turma=turma, eh_admin=True).count()
        if admins <= 1:
            return JsonResponse({
                'erro': 'Você é o único administrador. Não pode remover suas próprias permissões.'
            }, status=400)
    
    membro.eh_admin = False
    membro.save()
    
    return JsonResponse({
        'sucesso': True,
        'mensagem': f'{membro.usuario.email} não é mais administrador'
    })


@login_required
@require_http_methods(["POST"])
def sair_turma(request, id):
    """CDU-027: Sair da turma"""
    usuario = request.user
    turma = get_object_or_404(Turma, id=id)
    membro = get_object_or_404(MembroDeTurma, usuario=usuario, turma=turma)
    
    # Verificar se é o único admin
    if membro.eh_admin:
        admins = MembroDeTurma.objects.filter(turma=turma, eh_admin=True).count()
        if admins <= 1:
            return render(request, 'core/error.html', {
                'mensagem': 'Você é o único administrador. Transfira a administração antes de sair.'
            }, status=400)
    
    membro.delete()
    return redirect('inicio')


@login_required
def listar_membros_turma(request, id):
    """CDU-028: Listar membros da turma"""
    usuario = request.user
    turma = get_object_or_404(Turma, id=id)
    
    # Verificar se usuário é membro
    if not _usuario_eh_membro_turma(usuario, turma):
        return JsonResponse({'erro': 'Sem permissão'}, status=403)
    
    membros = MembroDeTurma.objects.filter(turma=turma).select_related('usuario')
    
    membros_data = [{
        'id': m.id,
        'email': m.usuario.email,
        'nome': m.usuario.primeiro_nome(),
        'eh_admin': m.eh_admin,
        'data_criacao': m.criado_em.isoformat()
    } for m in membros]
    
    return JsonResponse({
        'turma': turma.nome,
        'codigo': turma.codigo,
        'membros': membros_data,
        'total': len(membros_data)
    })
