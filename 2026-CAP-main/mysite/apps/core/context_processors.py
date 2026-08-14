from apps.calendarios.models import Calendario
from apps.calendarios.models import MembroDeCalendario
from apps.turmas.models import MembroDeTurma
from apps.turmas.models.turma import Turma


def _get_dados_calendarios_menu(request, turma=None):
    usuario = request.user
    calendarios_ocultos = request.session.get('calendarios_ocultos', [])
    calendarios_menu = []

    for membro in MembroDeCalendario.objects.filter(
        usuario=usuario, calendario__turma=turma
    ):
        calendario = membro.calendario
        preencher_botao = calendario.id not in calendarios_ocultos

        calendarios_menu.append( {
            'id': calendario.id,
            'nome': calendario.nome,
            'numero_paleta': membro.numero_paleta,
            'preencher_botao': preencher_botao,
        } )

    calendarios_menu = calendarios_menu or None

    return calendarios_menu


def get_calendarios_menu(request):
    if not request.user.is_authenticated:
        return {}

    calendarios_menu = _get_dados_calendarios_menu(request, turma=None)
    return {'calendarios_menu': calendarios_menu}


def get_turmas_menu(request):
    if not request.user.is_authenticated:
        return {}

    usuario = request.user
    turmas_ocultas = request.session.get('turmas_ocultas', [])
    turmas_menu = []

    for membro in MembroDeTurma.objects.filter(usuario=usuario):
        turma = membro.turma

        calendarios_turma = _get_dados_calendarios_menu(request, turma=turma)
        preencher_botao = turma.id not in turmas_ocultas

        turmas_menu.append( {
            'id': turma.id,
            'nome': turma.nome,
            'numero_paleta': membro.numero_paleta,
            'preencher_botao': preencher_botao,
            'calendarios': calendarios_turma
        } )

    turmas_menu = turmas_menu or None

    return {'turmas_menu': turmas_menu}