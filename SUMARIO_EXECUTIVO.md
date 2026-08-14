# SUMÁRIO EXECUTIVO - Projeto CAP

## 📊 Visão Geral Rápida

| Aspecto | Descrição |
|---------|-----------|
| **Nome** | CAP - Calendário Acadêmico de Prazos |
| **Objetivo** | Centralizar informações acadêmicas e permitir colaboração entre estudantes |
| **Linguagem** | Python (Django 6.0.6) |
| **Status Geral** | 🟡 Em Desenvolvimento (~36% completo) |
| **Tipo de Projeto** | Web App / MVP Educacional |

---

## 📁 Estrutura

**5 Apps Django:**
1. **usuarios** - Autenticação e perfil de usuários
2. **turmas** - Gerenciamento de turmas acadêmicas
3. **calendarios** - Calendários pessoais e de turma
4. **eventos** - Eventos nos calendários
5. **core** - Página inicial e funcionalidades centrais

---

## ✅ O que Funciona

| Funcionalidade | CDU | Status |
|---|---|---|
| Login/Logout | CDU-001, 002 | ✅ Pronto |
| Cadastro de Usuário | CDU-003 | ✅ Pronto |
| Criar Turma | CDU-017 | ✅ Pronto |
| Visualizar Turma | CDU-018 | ✅ Pronto |
| Deletar Turma | CDU-020 | ✅ Pronto |
| Criar Calendário | CDU-007 | ✅ Pronto |
| Visualizar Calendário | CDU-009 | ✅ Pronto |
| Deletar Calendário | CDU-011 | ✅ Pronto |
| Página Inicial (Calendário Semanal) | - | ✅ Pronto |

---

## ⚠️ O que Falta (Crítico)

### 🔴 BLOQUEIA O APLICATIVO
1. **Eventos não aparecem no calendário** (integração)
   - Eventos existem no banco, mas não são exibidos visualmente
   - Impacto: Funcionalidade central quebrada

2. **CRUD de Eventos incompleto** (CDU-012-016)
   - Criar: Parcial (apenas via POST)
   - Visualizar: Não existe
   - Atualizar: Não existe
   - Deletar: Não existe

3. **Gerenciar Participantes de Turma** (CDU-023-028)
   - Nenhuma das 6 operações implementada
   - Colaboração entre usuários não funciona

### 🟡 IMPORTANTE
4. **Perfil de Usuário** - Apenas shell vazio
5. **Atualizar Dados de Usuário** - Não implementado
6. **Atualizar Turma** - Apenas estrutura vazia
7. **Atualizar Calendário** - Apenas estrutura vazia
8. **Calendários de Turma** - Não há operações de add/remove

---

## 📊 Estatísticas de Implementação

### Por Módulo
```
AUTENTICAÇÃO       ████████░░  80%
USUÁRIOS           ████░░░░░░  20%
TURMAS             ██████░░░░  30%
CALENDÁRIOS        ██████░░░░  30%
EVENTOS            ███░░░░░░░  15%
CORE               ████████░░  40%
───────────────────────────
GERAL              ████░░░░░░  36%
```

### Por CDU
- ✅ Implementados: 9 CDUs (39%)
- ⏳ Parciais: 5 CDUs (22%)
- ❌ Não implementados: 12 CDUs (52%)
- ~~Removidos: 2 CDUs~~

---

## 🗄️ Banco de Dados

### Entidades Principais
- **Usuario**: Usuários do sistema (email, nome, permissões)
- **Turma**: Turmas acadêmicas (código auto-gerado)
- **Calendario**: Calendários pessoais ou de turma
- **Evento**: Eventos com data/hora
- **MembroDeTurma**: Relacionamento N:N (Usuário ↔ Turma)
- **MembroDeCalendario**: Relacionamento N:N (Usuário ↔ Calendário)

### Campos Padrão
Todas as entidades possuem:
- `criado_em` (timestamp automático)
- `alterado_em` (timestamp automático)

### Status da Documentação
- ❌ Diagrama ER: Não preenchido
- ❌ Modelo Relacional: Não preenchido
- ❌ Dicionário de Dados: Apenas template

---

## 📝 Documentação do Projeto

| Artefato | Status | Localização |
|----------|--------|-------------|
| Documento de Visão | ✅ v2.0 | doc/visao/doc-visao.md |
| Protótipos UI/UX | ✅ Disponível | doc/design/prototipos.md |
| Casos de Uso | ✅ 23 ativos | doc/cdu/ (29 arquivos) |
| Modelo de Domínio | ✅ Com diagrama | doc/dominio/dominio.md |
| Modelo de Dados | ⏳ Vazio | doc/bd/bd.md |
| Guia do Desenvolvedor | ✅ Completo | doc/guia-ds/guia.md |

---

## 👥 Equipe

5 desenvolvedores do IFRN
- André, Carlos, Giordanni, João, Bianca
- Repositório: GitHub (main branch)
- Workflow: Feature branches + Pull Requests

---

## 🎯 Recomendações Imediatas

### Fase 1 (CRÍTICO) - 1-2 semanas
1. Integrar eventos no calendário visual
2. Completar CRUD de eventos (CDU-012-016)
3. Implementar gerenciamento de participantes (CDU-023-028)

### Fase 2 (IMPORTANTE) - 1-2 semanas
4. Completar CRUD de usuários (CDU-004-006)
5. Completar operações de atualização (turmas, calendários)
6. Completar documentação do banco de dados

### Fase 3 (MELHORIAS) - 1 semana
7. Testes unitários e integração
8. Implementar sistema de cores (paleta)
9. Integrar modais nas páginas reais

---

## 📈 Métrica de Sucesso

```
Objetivo: Atingir 80% de completude no MVP

Progresso Atual: 36% ████░░░░░░░░░░░░░░░░░░
Alvo Fase 1:     65% ███████░░░░░░░░░░░░░░░
Alvo Fase 2:     80% ████████░░░░░░░░░░░░░░
Produção:        95% █████████░░░░░░░░░░░░░
```

---

**Para análise completa, consulte:** `/workspaces/teste-do-cap/ANALISE_PROJETO.md`
