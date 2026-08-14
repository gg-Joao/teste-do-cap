const calendarios = document.querySelectorAll('.item-menu.calendario')
const turmas = document.querySelectorAll('.item-menu.turma')

calendarios.forEach((calendario) => {
    const retorno = encodeURIComponent(window.location.pathname);
    const botaoMenu = calendario.querySelector(':scope > .botao-menu')
    const idCalendario = calendario.dataset.idCalendario

    botaoMenu.addEventListener('click', () => {
        event.preventDefault();
        event.stopPropagation();
        window.location.href = `/alterar_visibilidade_calendario/${idCalendario}?next=${retorno}`;
    })
})

turmas.forEach((turma) => {
    const retorno = encodeURIComponent(window.location.pathname);
    const botaoMenu = turma.querySelector(':scope > .botao-menu')
    const idTurma = turma.dataset.idTurma

    botaoMenu.addEventListener('click', () => {
        event.preventDefault();
        event.stopPropagation();
        window.location.href = `/alterar_visibilidade_turma/${idTurma}?next=${retorno}`;
    })
})