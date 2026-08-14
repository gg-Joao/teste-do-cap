from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.calendarios.models import Calendario, MembroDeCalendario
from apps.usuarios.models import Usuario


def _usuario_eh_admin_calendario(usuario, calendario):
    """Verifica se usuário é admin do calendário"""
    membro = MembroDeCalendario.objects.filter(
        usuario=usuario,
        calendario=calendario
    ).first()
    return membro and membro.eh_admin


def _usuario_eh_membro_calendario(usuario, calendario):
    """Verifica se usuário é membro do calendário"""
    return MembroDeCalendario.objects.filter(
        usuario=usuario,
        calendario=calendario
    ).exists()


@login_required
def calendario_detalhe(request, id):
    """CDU-009: Visualizar calendário"""
    usuario = request.user
    calendario = get_object_or_404(Calendario, id=id)
    
    # Verificar se usuário é membro
    if not _usuario_eh_membro_calendario(usuario, calendario):
        return render(request, 'core/error.html', {
            'mensagem': 'Você não tem acesso a este calendário.'
        }, status=403)
    
    membro = MembroDeCalendario.objects.get(usuario=usuario, calendario=calendario)
    membros_calendario = MembroDeCalendario.objects.filter(calendario=calendario)

    lideres = [
        {
            'id': membro.id,
            'nome': membro.usuario.nome_completo,
            'email': membro.usuario.email,
            'paleta': membro.numero_paleta
        }
        for membro in membros_calendario.filter(eh_admin=True)
    ]
    membros_comuns = [
        {
            'id': membro.id,
            'nome': membro.usuario.nome_completo,
            'email': membro.usuario.email,
            'paleta': membro.numero_paleta
        }
        for membro in membros_calendario.filter(eh_admin=False)
    ]

    # Recuperar eventos
    eventos = calendario.eventos.all().order_by('inicio')

    calendario_context = {
        'id': calendario.id,
        'nome': calendario.nome,
        'descricao': calendario.descricao,
        'turma': calendario.turma,
        'lideres': lideres,
        'membros_comuns': membros_comuns,
        'total_membros': membros_calendario.count(),
        'criado_em': calendario.criado_em
    }
    usuario_context = {
        'nome': request.user.nome_completo,
        'email': request.user.email,
        'eh_admin': membro.eh_admin,
        'paleta': membro.numero_paleta
    }

    context = {
        'calendario': calendario_context,
        'usuario': usuario_context,
        'eventos': eventos,
        'pode_gerenciar': membro.eh_admin
    }
    return render(request, 'calendarios/calendario.html', context)


@login_required
def criar_calendario(request):
    """CDU-007: Criar calendário"""
    usuario = request.user

    # Gerar nome único
    numero_calendario = 1
    while True:
        if not usuario.calendarios.filter(turma=None, nome__icontains=f'Calendário {numero_calendario}'):
            break
        numero_calendario += 1
    nome_calendario = f'Calendário {numero_calendario}'

    # Criar calendário
    calendario = Calendario.objects.create(
        nome=nome_calendario,
        descricao=f'Bem vindo a {nome_calendario}!'
    )

    # Adicionar criador como admin
    numero_paleta = usuario.paleta_menos_usada()
    MembroDeCalendario.objects.create(
        usuario=usuario,
        calendario=calendario,
        eh_admin=True,
        numero_paleta=numero_paleta
    )

    return redirect('calendarios:calendario_detalhe', calendario.id)


@login_required
@require_http_methods(["GET", "POST"])
def atualizar_calendario(request, id):
    """CDU-010: Atualizar calendário"""
    usuario = request.user
    calendario = get_object_or_404(Calendario, id=id)
    
    # Verificar permissões
    if not _usuario_eh_admin_calendario(usuario, calendario):
        return render(request, 'core/error.html', {
            'mensagem': 'Apenas administradores podem editar este calendário.'
        }, status=403)
    
    if request.method == 'GET':
        return render(request, 'calendarios/editar_calendario.html', {
            'calendario': calendario
        })
    
    # POST - Atualizar calendário
    try:
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        
        if not nome:
            raise ValidationError('Nome do calendário é obrigatório.')
        
        calendario.nome = nome
        calendario.descricao = descricao
        calendario.save()
        
        return redirect('calendarios:calendario_detalhe', calendario.id)
    
    except ValidationError as e:
        return render(request, 'calendarios/editar_calendario.html', {
            'calendario': calendario,
            'error': str(e)
        })


@login_required
@require_http_methods(["POST"])
def deletar_calendario(request, id):
    """CDU-011: Deletar calendário"""
    usuario = request.user
    calendario = get_object_or_404(Calendario, id=id)
    
    # Verificar permissões
    if not _usuario_eh_admin_calendario(usuario, calendario):
        return render(request, 'core/error.html', {
            'mensagem': 'Apenas administradores podem deletar este calendário.'
        }, status=403)
    
    calendario.delete()
    return redirect('inicio')


@login_required
@require_http_methods(["POST"])
def adicionar_membro_calendario(request, id):
    """Adicionar membro ao calendário"""
    usuario = request.user
    calendario = get_object_or_404(Calendario, id=id)
    
    # Verificar permissões
    if not _usuario_eh_admin_calendario(usuario, calendario):
        return JsonResponse({'erro': 'Sem permissão'}, status=403)
    
    try:
        email = request.POST.get('email', '').strip()
        
        if not email:
            return JsonResponse({'erro': 'Email é obrigatório'}, status=400)
        
        novo_usuario = get_object_or_404(Usuario, email=email)
        
        # Verificar se já é membro
        if _usuario_eh_membro_calendario(novo_usuario, calendario):
            return JsonResponse({
                'erro': 'Usuário já é membro deste calendário'
            }, status=400)
        
        # Adicionar membro
        numero_paleta = novo_usuario.paleta_menos_usada()
        MembroDeCalendario.objects.create(
            usuario=novo_usuario,
            calendario=calendario,
            eh_admin=False,
            numero_paleta=numero_paleta
        )
        
        return JsonResponse({
            'sucesso': True,
            'mensagem': f'{novo_usuario.email} foi adicionado ao calendário'
        })
    
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def remover_membro_calendario(request, id, membro_id):
    """Remover membro do calendário"""
    usuario = request.user
    calendario = get_object_or_404(Calendario, id=id)
    membro = get_object_or_404(MembroDeCalendario, id=membro_id, calendario=calendario)
    
    # Verificar permissões
    if not _usuario_eh_admin_calendario(usuario, calendario):
        return JsonResponse({'erro': 'Sem permissão'}, status=403)
    
    # Não permitir remover a si mesmo se for o único admin
    if membro.usuario == usuario:
        admins = MembroDeCalendario.objects.filter(calendario=calendario, eh_admin=True).count()
        if admins <= 1:
            return JsonResponse({
                'erro': 'Você é o único administrador. Não pode remover a si mesmo.'
            }, status=400)
    
    membro_removido = membro.usuario.email
    membro.delete()
    
    return JsonResponse({
        'sucesso': True,
        'mensagem': f'{membro_removido} foi removido do calendário'
    })


@login_required
@require_http_methods(["POST"])
def tornar_admin_calendario(request, id, membro_id):
    """Tornar membro admin do calendário"""
    usuario = request.user
    calendario = get_object_or_404(Calendario, id=id)
    membro = get_object_or_404(MembroDeCalendario, id=membro_id, calendario=calendario)
    
    # Verificar permissões
    if not _usuario_eh_admin_calendario(usuario, calendario):
        return JsonResponse({'erro': 'Sem permissão'}, status=403)
    
    membro.eh_admin = True
    membro.save()
    
    return JsonResponse({
        'sucesso': True,
        'mensagem': f'{membro.usuario.email} agora é administrador'
    })


@login_required
@require_http_methods(["POST"])
def remover_admin_calendario(request, id, membro_id):
    """Remover permissão de admin"""
    usuario = request.user
    calendario = get_object_or_404(Calendario, id=id)
    membro = get_object_or_404(MembroDeCalendario, id=membro_id, calendario=calendario)
    
    # Verificar permissões
    if not _usuario_eh_admin_calendario(usuario, calendario):
        return JsonResponse({'erro': 'Sem permissão'}, status=403)
    
    # Não permitir remover a si mesmo se for o único admin
    if membro.usuario == usuario:
        admins = MembroDeCalendario.objects.filter(calendario=calendario, eh_admin=True).count()
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

