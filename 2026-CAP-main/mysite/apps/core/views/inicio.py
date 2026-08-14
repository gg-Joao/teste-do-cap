from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q

from apps.calendarios.models import Calendario
from apps.eventos.models import Evento


MESES_ptbr = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril',
    'Maio', 'Junho', 'Julho', 'Agosto',
    'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

DIAS_SEMANA_ptbr = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']


def get_dia_em_foco(request) -> date:
    dia_em_foco_str = request.session.setdefault(
        'dia_em_foco',
        timezone.localdate().isoformat()
    )
    return date.fromisoformat(dia_em_foco_str)


def set_dia_em_foco(request, dia_em_foco: date) -> None:
    request.session['dia_em_foco'] = dia_em_foco.isoformat()


def _get_eventos_semana(usuario, primeira_data_semana: date, ultima_data_semana: date):
    """Recupera eventos do usuário para a semana especificada."""
    calendarios = Calendario.objects.filter(
        Q(usuarios=usuario) | Q(turma__usuarios=usuario)
    ).distinct()

    inicio_semana = datetime.combine(primeira_data_semana, datetime.min.time())
    fim_semana = datetime.combine(ultima_data_semana, datetime.max.time())

    eventos = Evento.objects.filter(
        calendario__in=calendarios,
        inicio__gte=inicio_semana,
        inicio__lte=fim_semana
    ).select_related('calendario').order_by('inicio')

    eventos_semana = []
    for evento in eventos:
        duracao_minutos = int((evento.fim - evento.inicio).total_seconds() / 60)
        data_iso = evento.inicio.date().isoformat()
        hora_inicio = evento.inicio.hour
        hora_fim = evento.fim.hour

        eventos_semana.append({
            'id': evento.id,
            'nome': evento.nome,
            'conteudo': evento.conteudo,
            'inicio': evento.inicio.isoformat(),
            'fim': evento.fim.isoformat(),
            'hora_inicio': evento.inicio.strftime('%H:%M'),
            'hora_fim': evento.fim.strftime('%H:%M'),
            'duracao_minutos': duracao_minutos,
            'data_iso': data_iso,
            'coluna': (evento.inicio.date() - primeira_data_semana).days + 1,
            'linha': hora_inicio + 1,
            'altura': max(1, duracao_minutos / 60),
            'calendario': evento.calendario.nome,
            'paleta': getattr(evento.calendario, 'numero_paleta', 1),
        })

    return eventos_semana


@login_required
def inicio(request):
    dia_em_foco = get_dia_em_foco(request)
    mes_em_foco = MESES_ptbr[dia_em_foco.month - 1]
    ano_em_foco = dia_em_foco.year

    dias_ate_domingo = (dia_em_foco.weekday() + 1) % 7
    ultimo_domingo = dia_em_foco - timedelta(days=dias_ate_domingo)

    datas_calendario_geral = []
    for i in range(7):
        data = ultimo_domingo + timedelta(days=i)
        nome = f'{DIAS_SEMANA_ptbr[data.weekday()]} {data.day:02}'

        datas_calendario_geral.append( {
            'nome': nome,
            'isoformat': data.isoformat(),
        } )

    horarios_calendario_geral = [f'{i:02}:00' for i in range(24)]
    
    # Recuperar eventos da semana
    proxima_segunda = ultimo_domingo + timedelta(days=1)
    ultimo_sabado = ultimo_domingo + timedelta(days=6)
    eventos_semana = _get_eventos_semana(request.user, ultimo_domingo, ultimo_sabado)

    context = {
        'dia_em_foco': dia_em_foco,
        'mes_em_foco': mes_em_foco,
        'ano_em_foco': ano_em_foco,
        'datas_calendario_geral': datas_calendario_geral,
        'horarios_calendario_geral': horarios_calendario_geral,
        'eventos_semana': eventos_semana,
    }

    return render(request, 'core/inicio.html', context)



def semana_anterior(request):    
    dia_em_foco = get_dia_em_foco(request)
    set_dia_em_foco(request, dia_em_foco - timedelta(days=7))
    return redirect('inicio')


def proxima_semana(request):
    dia_em_foco = get_dia_em_foco(request)
    set_dia_em_foco(request, dia_em_foco + timedelta(days=7))
    return redirect('inicio')


def voltar_para_hoje(request):
    set_dia_em_foco(request, timezone.localdate())
    return redirect('inicio')