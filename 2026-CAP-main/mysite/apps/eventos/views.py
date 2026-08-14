from datetime import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from apps.calendarios.models import Calendario, MembroDeCalendario
from apps.eventos.models import Evento
from apps.turmas.models import MembroDeTurma


def _usuario_pode_editar_evento(usuario, evento):
    """Verifica se o usuário pode editar um evento"""
    # Evento em calendário pessoal
    membro = MembroDeCalendario.objects.filter(
        usuario=usuario,
        calendario=evento.calendario
    ).first()
    if membro and membro.eh_admin:
        return True
    
    # Evento em calendário de turma
    turma = evento.calendario.turma
    if turma:
        membro_turma = MembroDeTurma.objects.filter(
            usuario=usuario,
            turma=turma
        ).first()
        if membro_turma and membro_turma.eh_admin:
            return True
    
    return False


@login_required
@require_http_methods(["GET", "POST"])
def criar_evento(request):
    """CDU-012: Criar evento"""
    if request.method == 'GET':
        # Recuperar calendários disponíveis para o usuário (aqueles que o usuário é admin)
        from apps.calendarios.models import MembroDeCalendario
        from apps.turmas.models import Turma, MembroDeTurma
        
        # Calendários pessoais onde é admin
        cal_pessoais = MembroDeCalendario.objects.filter(
            usuario=request.user,
            eh_admin=True
        ).values_list('calendario_id', flat=True)
        
        # Calendários de turmas onde é admin
        turmas_admin = MembroDeTurma.objects.filter(
            usuario=request.user,
            eh_admin=True
        ).values_list('turma_id', flat=True)
        cal_turmas = Calendario.objects.filter(turma_id__in=turmas_admin).values_list('id', flat=True)
        
        # Todos os calendários onde o usuário é admin
        calendarios = Calendario.objects.filter(
            id__in=list(cal_pessoais) + list(cal_turmas)
        ).distinct()
        
        return render(request, 'eventos/criar_evento.html', {
            'calendarios': calendarios
        })
    
    # POST - Criar novo evento
    try:
        titulo = request.POST.get('titulo', '').strip()
        calendario_id = request.POST.get('calendario')
        data = request.POST.get('data')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')
        descricao = request.POST.get('descricao', '').strip()

        # Validações
        if not titulo:
            raise ValidationError('Título do evento é obrigatório.')
        if not calendario_id:
            raise ValidationError('Calendário é obrigatório.')
        if not data or not inicio or not fim:
            raise ValidationError('Data e horários são obrigatórios.')

        # Verificar permissões
        calendario = get_object_or_404(Calendario, pk=calendario_id)
        if not _usuario_pode_editar_evento(request.user, 
                                          Evento(calendario=calendario)):
            return render(request, 'eventos/criar_evento.html', {
                'error': 'Você não tem permissão para criar eventos neste calendário.',
                'calendarios': Calendario.objects.filter(usuarios=request.user)
            })

        # Criar evento
        try:
            inicio_dt = datetime.fromisoformat(f"{data}T{inicio}")
            fim_dt = datetime.fromisoformat(f"{data}T{fim}")
            evento = Evento(
                nome=titulo,
                conteudo=descricao,
                inicio=inicio_dt,
                fim=fim_dt,
                calendario=calendario,
            )
            evento.full_clean()
            evento.save()
            return redirect('eventos:evento_detalhe', evento.pk)
        except (ValueError, ValidationError) as e:
            raise ValidationError(f'Erro ao criar evento: {str(e)}')

    except ValidationError as e:
        calendarios = Calendario.objects.filter(usuarios=request.user)
        return render(request, 'eventos/criar_evento.html', {
            'error': str(e),
            'calendarios': calendarios
        })


@login_required
def evento_detalhe(request, pk):
    """CDU-013: Visualizar evento"""
    evento = get_object_or_404(Evento, pk=pk)
    
    # Verificar se usuário pode visualizar
    calendarios = Calendario.objects.filter(
        Q(usuarios=request.user) | Q(turma__usuarios=request.user)
    )
    if evento.calendario not in calendarios:
        return render(request, 'error.html', {
            'mensagem': 'Você não tem permissão para visualizar este evento.'
        }, status=403)
    
    pode_editar = _usuario_pode_editar_evento(request.user, evento)
    
    return render(request, 'eventos/detalhe_evento.html', {
        'evento': evento,
        'pode_editar': pode_editar
    })


@login_required
@require_http_methods(["GET", "POST"])
def atualizar_evento(request, pk):
    """CDU-014: Atualizar evento"""
    evento = get_object_or_404(Evento, pk=pk)
    
    # Verificar permissões
    if not _usuario_pode_editar_evento(request.user, evento):
        return render(request, 'error.html', {
            'mensagem': 'Você não tem permissão para editar este evento.'
        }, status=403)
    
    if request.method == 'GET':
        calendarios = Calendario.objects.filter(
            Q(usuarios=request.user) | Q(turma__usuarios=request.user)
        ).distinct()
        return render(request, 'eventos/editar_evento.html', {
            'evento': evento,
            'calendarios': calendarios
        })
    
    # POST - Atualizar evento
    try:
        titulo = request.POST.get('titulo', '').strip()
        calendario_id = request.POST.get('calendario')
        data = request.POST.get('data')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')
        descricao = request.POST.get('descricao', '').strip()

        if not titulo or not calendario_id or not data or not inicio or not fim:
            raise ValidationError('Todos os campos são obrigatórios.')

        novo_calendario = get_object_or_404(Calendario, pk=calendario_id)
        
        evento.nome = titulo
        evento.conteudo = descricao
        evento.calendario = novo_calendario
        evento.inicio = datetime.fromisoformat(f"{data}T{inicio}")
        evento.fim = datetime.fromisoformat(f"{data}T{fim}")
        
        evento.full_clean()
        evento.save()
        
        return redirect('eventos:evento_detalhe', evento.pk)
    
    except ValidationError as e:
        calendarios = Calendario.objects.filter(usuarios=request.user)
        return render(request, 'eventos/editar_evento.html', {
            'evento': evento,
            'calendarios': calendarios,
            'error': str(e)
        })


@login_required
@require_http_methods(["POST"])
def deletar_evento(request, pk):
    """CDU-016: Deletar evento"""
    evento = get_object_or_404(Evento, pk=pk)
    
    # Verificar permissões
    if not _usuario_pode_editar_evento(request.user, evento):
        return render(request, 'error.html', {
            'mensagem': 'Você não tem permissão para deletar este evento.'
        }, status=403)
    
    calendario_id = evento.calendario.id
    evento.delete()
    
    return redirect('calendarios:calendario_detalhe', calendario_id)


def teste_modal(request):
    return render(request, 'eventos/teste_modal.html', {})

