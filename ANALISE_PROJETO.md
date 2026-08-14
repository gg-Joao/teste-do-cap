# Análise Completa do Projeto CAP - Calendário Acadêmico de Prazos

## 📋 Sumário Executivo

O **CAP (Calendário Acadêmico de Prazos)** é uma aplicação web desenvolvida em **Django** com o objetivo de centralizar informações acadêmicas e permitir que estudantes gerenciem colaborativamente eventos, tarefas e cronogramas de suas turmas. O projeto está em fase de desenvolvimento, com modelos de dados bem estruturados, mas com funcionalidades incompletas em várias áreas.

---

## 1. Estrutura Geral do Projeto (Arquitetura)

### 1.1 Organização de Diretórios

```
2026-CAP-main/
├── doc/                          # Documentação do projeto
│   ├── arquivo_astah/            # Diagramas UML
│   ├── bd/                        # Documentação do banco de dados
│   ├── cdu/                       # Casos de Uso (29 CDUs documentados)
│   ├── design/                    # Design UI/UX, logo, paleta de cores
│   ├── dominio/                   # Modelo de domínio e diagrama de classes
│   ├── guia-ds/                   # Guia do desenvolvedor
│   └── visao/                     # Documento de visão do projeto
├── mysite/                        # Aplicação Django principal
│   ├── apps/                      # Aplicações Django
│   │   ├── calendarios/           # App de gerenciamento de calendários
│   │   ├── core/                  # App central (autenticação, página inicial)
│   │   ├── eventos/               # App de gerenciamento de eventos
│   │   ├── turmas/                # App de gerenciamento de turmas
│   │   └── usuarios/              # App de gerenciamento de usuários
│   ├── config/                    # Configuração do Django
│   │   ├── settings/              # Development, Production, Testing
│   │   ├── urls.py                # Roteamento principal
│   │   ├── wsgi.py                # WSGI
│   │   └── asgi.py                # ASGI
│   └── manage.py                  # CLI do Django
├── requirements.txt               # Dependências do projeto
└── README.md                       # Documentação principal
```

### 1.2 Padrão Arquitetural

- **Padrão MVC (Model-View-Controller)**: Implementado naturalmente pelo Django
- **Estrutura Modular**: 5 apps Django independentes
- **Separação de Responsabilidades**: Cada app gerencia um domínio específico
- **ORM Django**: Utiliza Django ORM para abstração do banco de dados

---

## 2. Propósito e Escopo do Projeto

### 2.1 Objetivo Geral

Centralizar em um único ambiente web as informações acadêmicas importantes para estudantes (prazos, materiais, cronogramas), permitindo:
- Organização independente de cronogramas e eventos
- Collaboração entre estudantes de uma mesma turma
- Protagonismo estudantil na organização da vida escolar
- Conciliação entre deveres escolares e vida pessoal

### 2.2 Problema que Resolve

| Aspecto | Descrição |
|---------|-----------|
| **Problema** | Ausência de local adequado para organizar informações acadêmicas; dispersão entre plataformas (Google Classroom, SUAP, e-mail, etc.) |
| **Impactos** | Desorganização acadêmica, perda de prazos, acompanhamento deficiente |
| **Solução** | Sistema web unificado para calendários pessoais e acadêmicos |

### 2.3 Usuários Alvo

1. **Aluno**: Visualizar atividades, materiais, cronogramas; organizar calendário pessoal
2. **Representante/Líder de Turma**: Validar e atualizar informações; manter sistema atualizado

### 2.4 Requisitos Principais (Documento de Visão v2.0)

**Requisitos Funcionais (Alta Prioridade):**
- RF01: Gerir conta (criar, visualizar, atualizar, deletar)
- RF02: Autenticação (login/logout)
- RF03: Gerir calendário (pessoal e acadêmico)
- RF04: Gerir calendário da turma
- RF05: Gerir evento de calendário
- RF06: Gerir turma
- RF07: Gerir membro de turma (permissões)
- RF08: Gerir inscrições em turma

**Requisitos Não-Funcionais:**
- Performance: Carregar eventos em até 10 segundos
- Usabilidade: Interface objetiva e clara
- Segurança: Dados pessoais criptografados
- Disponibilidade: 24h de uptime

---

## 3. Tecnologias Utilizadas

### 3.1 Stack Tecnológico

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| **Backend** | Django | 6.0.6 |
| **Linguagem** | Python | 3.x |
| **Servidor WSGI** | ASGI/WSGI | - |
| **Banco de Dados** | SQLite (dev) | - |
| **ORM** | Django ORM | Nativo |
| **Imagens** | Pillow | 12.2.0 |
| **Parsing SQL** | sqlparse | 0.5.5 |
| **Timezone** | tzdata | 2026.2 |
| **Frontend** | HTML/CSS/JavaScript | - |

### 3.2 Dependências (requirements.txt)

```
asgiref==3.11.1
Django==6.0.6
pillow==12.2.0
sqlparse==0.5.5
tzdata==2026.2
```

### 3.3 Ambiente

- **SO**: Ubuntu 24.04.4 LTS (Dev Container)
- **Git**: Controle de versão
- **GitHub**: Repositório remoto

---

## 4. Aplicações Django (Apps)

### 4.1 Visão Geral

O projeto está organizado em **5 aplicações Django** independentes:

```
apps/
├── calendarios/    → Gerenciamento de calendários pessoais e acadêmicos
├── core/           → Funcionalidade central e autenticação
├── eventos/        → Criação e gerenciamento de eventos
├── turmas/         → Criação e gerenciamento de turmas
└── usuarios/       → Gestão de usuários e autenticação
```

### 4.2 App: **USUARIOS** (Gerenciamento de Usuários)

**Modelos:**
- `Usuario`: Usuário do sistema (estende `AbstractBaseUser`)
  - `email` (unique)
  - `nome_completo`
  - `is_active`, `is_staff` (permissões)
  - Método `paleta_menos_usada()`: Retorna paleta de cores menos usada
  - Método `primeiro_nome()`: Extrai primeiro nome

- `UsuarioManager`: Manager customizado para criar usuários

**Views Implementadas:**
- `login_view()`: Autenticação de usuário (CDU-001)
- `logout_view()`: Saída do sistema (CDU-002)
- `cadastro()`: Criação de nova conta (CDU-003)
- `perfil()`: Visualizar perfil do usuário (CDU-004)

**Templates:**
- `login.html`: Formulário de login
- `cadastro.html`: Formulário de cadastro
- `perfil.html`: Página de perfil (vazio)

**Status de Implementação:** ⚠️ **PARCIAL**
- ✅ Login/Logout implementados
- ✅ Cadastro implementado
- ⏳ Atualizar conta (vazio)
- ⏳ Deletar conta (não implementado)
- ⏳ Perfil (apenas shell vazio)

---

### 4.3 App: **TURMAS** (Gerenciamento de Turmas)

**Modelos:**
- `Turma`: Representa uma turma acadêmica
  - `nome` (CharField)
  - `descricao` (CharField)
  - `codigo` (unique, gerado automaticamente - 6 caracteres alphanumério)
  - ManyToMany com `Usuario` através de `MembroDeTurma`
  - Método `gerar_codigo_turma()`: Gera código único com retry

- `MembroDeTurma`: Relacionamento entre Usuário e Turma
  - `eh_admin` (Boolean)
  - `numero_paleta` (PositiveIntegerField, 0-9)
  - FK: `usuario`, `turma`
  - Constraint: Única combinação usuario-turma

**Views Implementadas:**
- `turma()`: Visualizar detalhes de turma (CDU-018)
- `criar_turma()`: Criar nova turma (CDU-017)
- `atualizar_turma()`: Atualizar turma (CDU-019) - **INCOMPLETO**
- `deletar_turma()`: Deletar turma (CDU-020)

**Templates:**
- `turma.html`: Página de visualização de turma

**Status de Implementação:** ⚠️ **PARCIAL**
- ✅ Criar turma implementado
- ✅ Visualizar turma implementado
- ⏳ Atualizar turma (apenas estrutura `if membro.eh_admin: ...`)
- ✅ Deletar turma implementado (validação admin)
- ⏳ Adicionar/Remover calendário de turma (CDU-021, CDU-022) - não implementado
- ⏳ Remover participante (CDU-024) - não implementado
- ⏳ Alterar permissão (CDU-025) - não implementado

---

### 4.4 App: **CALENDARIOS** (Gerenciamento de Calendários)

**Modelos:**
- `Calendario`: Calendário pessoal ou acadêmico
  - `nome` (CharField)
  - `descricao` (CharField)
  - `turma` (ForeignKey, nullable - permite calendários pessoais)
  - ManyToMany com `Usuario` através de `MembroDeCalendario`

- `MembroDeCalendario`: Relacionamento entre Usuário e Calendário
  - `eh_admin` (Boolean)
  - `numero_paleta` (PositiveIntegerField, 0-9)
  - FK: `usuario`, `calendario`
  - Constraint: Única combinação usuario-calendario

**Views Implementadas:**
- `calendario()`: Visualizar calendário (CDU-009)
- `criar_calendario()`: Criar novo calendário pessoal (CDU-007)
- `atualizar_calendario()`: Atualizar calendário (CDU-010) - **INCOMPLETO**
- `deletar_calendario()`: Deletar calendário (CDU-011)

**Templates:**
- `calendario.html`: Página de visualização de calendário com membros e líderes

**Status de Implementação:** ⚠️ **PARCIAL**
- ✅ Criar calendário implementado
- ✅ Visualizar calendário implementado
- ⏳ Atualizar calendário (apenas estrutura)
- ✅ Deletar calendário implementado (validação admin)

---

### 4.5 App: **EVENTOS** (Gerenciamento de Eventos)

**Modelos:**
- `Evento`: Evento em um calendário
  - `nome` (CharField)
  - `conteudo` (CharField, descritivo)
  - `inicio` (DateTimeField, validado entre 2000-2050)
  - `fim` (DateTimeField, validado entre 2000-2050)
  - FK: `calendario`
  - Validações: evento no mesmo dia, fim > início

**Views Implementadas:**
- `criar_evento()`: Criar novo evento (CDU-012) - **PARCIALMENTE**
- `teste_modal()`: Página de teste para modais
- Outras visualizações (CDU-013, CDU-014, CDU-015, CDU-016) - **NÃO IMPLEMENTADAS**

**Templates:**
- `modal_criar_evento.html`: Modal para criar evento
- `modal_editar_evento.html`: Modal para editar evento
- `modal_vizualizar_evento.html`: Modal para visualizar evento
- `teste_modal.html`: Página de teste

**Status de Implementação:** ⏳ **MUITO INCOMPLETO**
- ⏳ Criar evento (view parcial, validação simples)
- ⏳ Visualizar quadro geral (CDU-013) - não implementado
- ⏳ Visualizar evento (CDU-014) - não implementado
- ⏳ Atualizar evento (CDU-015) - não implementado
- ⏳ Deletar evento (CDU-016) - não implementado

**Observação:** Existe arquivo `calendarios_context.py` não documentado

---

### 4.6 App: **CORE** (Funcionalidade Central)

**Modelos:**
- `BaseModel`: Classe abstrata com campos de auditoria
  - `criado_em` (DateTimeField, auto_now_add)
  - `alterado_em` (DateTimeField, auto_now)

**Views Implementadas:**
- `inicio()`: Página inicial com calendário semanal (CDU-Inicio)
- `semana_anterior()`: Navegar para semana anterior
- `proxima_semana()`: Navegar para próxima semana
- `voltar_para_hoje()`: Retornar ao dia atual

**Templates:**
- `base.html`: Template base com herança
- `inicio.html`: Página inicial com calendário
- `menu_lateral.html`: Menu de navegação lateral

**Views Vazios:**
- `views.py`: Arquivo vazio (views.py)

**Status de Implementação:** ✅ **PARCIALMENTE COMPLETO**
- ✅ Página inicial com calendário semanal
- ✅ Navegação de semanas
- ⏳ Integração com eventos do usuário (não mostrados no calendário)

---

## 5. Estrutura do Banco de Dados

### 5.1 Entidades Principais (Modelo de Dados)

| Entidade | Descrição |
|----------|-----------|
| **Usuario** | Usuários do sistema (estudantes, líderes) |
| **Turma** | Turmas acadêmicas |
| **Calendario** | Calendários pessoais ou vinculados a turmas |
| **Evento** | Eventos dentro de um calendário |
| **MembroDeTurma** | Relacionamento N:N entre Usuário e Turma |
| **MembroDeCalendario** | Relacionamento N:N entre Usuário e Calendario |

### 5.2 Diagrama ER (Simplificado)

```
┌─────────────┐
│   Usuario   │
├─────────────┤
│ id (PK)     │
│ email*      │
│ nome_compl  │
│ is_active   │
│ is_staff    │
└─────────────┘
       │
       │ 1:N (através de MembroDeTurma)
       │
┌──────────────────┐
│ MembroDeTurma    │
├──────────────────┤
│ usuario_id (FK)  │
│ turma_id (FK)    │
│ eh_admin         │
│ numero_paleta    │
└──────────────────┘
       │
       │ N:1
       │
┌─────────────┐
│   Turma     │
├─────────────┤
│ id (PK)     │
│ nome        │
│ descricao   │
│ codigo*     │
└─────────────┘
       │
       │ 1:N
       │
┌─────────────────┐
│  Calendario     │
├─────────────────┤
│ id (PK)         │
│ nome            │
│ descricao       │
│ turma_id (FK)*  │
└─────────────────┘
       │
       │ 1:N
       │
┌──────────────────────┐
│ MembroDeCalendario   │
├──────────────────────┤
│ usuario_id (FK)      │
│ calendario_id (FK)   │
│ eh_admin             │
│ numero_paleta        │
└──────────────────────┘
       │
       │ N:1
       │
  Usuario
```

### 5.3 Regras de Negócio (RN)

| Código | Regra | Status |
|--------|-------|--------|
| **RN01** | Associação de Evento ao Calendário | ✅ Implementada |
| **RN02** | Herança de Cor do Calendário | ⏳ Não implementada (via paleta) |
| **RN03** | Existência de Administrador | ✅ Validada em criação |

### 5.4 Campos de Auditoria

Todas as entidades principais herdam `BaseModel`:
- `criado_em`: Timestamp de criação (auto_now_add)
- `alterado_em`: Timestamp de última modificação (auto_now)

### 5.5 Status da Documentação do BD

📄 **Documento `/doc/bd/bd.md`:** ⏳ **INCOMPLETO**
- ❌ Diagrama ER não preenchido (placeholder)
- ❌ Modelo Relacional não preenchido (placeholder)
- ❌ Dicionário de Dados vazio (apenas template)

---

## 6. Casos de Uso (CDUs) - 29 Documentados

### 6.1 Distribuição por Módulo

| Módulo | CDUs | Status |
|--------|------|--------|
| **Autenticação** | CDU-001, CDU-002 | ✅ Implementado |
| **Conta** | CDU-003, CDU-004, CDU-005, CDU-006 | ⏳ Parcial |
| **Calendários** | CDU-007, CDU-009, CDU-010, CDU-011 | ⚠️ Parcial |
| **Eventos** | CDU-012, CDU-013, CDU-014, CDU-015, CDU-016 | ⏳ Incompleto |
| **Turmas** | CDU-017, CDU-018, CDU-019, CDU-020, CDU-021, CDU-022 | ⚠️ Parcial |
| **Participação Turmas** | CDU-023, CDU-024, CDU-025, CDU-026, CDU-027, CDU-028 | ⏳ Incompleto |

### 6.2 Lista Completa de CDUs

#### **AUTENTICAÇÃO** (2 CDUs)
- ✅ **CDU-001**: Entrar - Autenticar usuário
- ✅ **CDU-002**: Sair - Fazer logout

#### **CONTA** (4 CDUs)
- ✅ **CDU-003**: Criar conta - Cadastrar novo usuário
- ⏳ **CDU-004**: Visualizar conta - Ver dados da conta (parcial)
- ⏳ **CDU-005**: Atualizar conta - Editar informações (não implementado)
- ⏳ **CDU-006**: Deletar conta - Remover conta (não implementado)

#### **CALENDÁRIOS** (4 CDUs)
- ✅ **CDU-007**: Criar calendário - Novo calendário pessoal
- ~~CDU-008~~: Consultar calendários (removido v4)
- ✅ **CDU-009**: Visualizar calendário - Ver detalhes
- ⏳ **CDU-010**: Atualizar calendário - Editar (não implementado)
- ✅ **CDU-011**: Deletar calendário - Remover

#### **EVENTOS** (5 CDUs)
- ⏳ **CDU-012**: Criar evento - Adicionar evento (parcial)
- ⏳ **CDU-013**: Visualizar quadro geral - Ver todos os eventos (não implementado)
- ⏳ **CDU-014**: Visualizar evento - Ver detalhes do evento (não implementado)
- ⏳ **CDU-015**: Atualizar evento - Editar evento (não implementado)
- ⏳ **CDU-016**: Deletar evento - Remover evento (não implementado)

#### **TURMAS** (6 CDUs)
- ✅ **CDU-017**: Criar turma - Nova turma acadêmica
- ✅ **CDU-018**: Visualizar turma - Ver detalhes
- ⏳ **CDU-019**: Atualizar turma - Editar (não implementado)
- ✅ **CDU-020**: Deletar turma - Remover
- ⏳ **CDU-021**: Adicionar calendário à turma (não implementado)
- ⏳ **CDU-022**: Remover calendário de turma (não implementado)
- ~~CDU-029~~: Consultar turmas (removido v4)

#### **PARTICIPAÇÃO EM TURMAS** (6 CDUs)
- ⏳ **CDU-023**: Consultar participantes de turma (não implementado)
- ⏳ **CDU-024**: Remover participante de turma (não implementado)
- ⏳ **CDU-025**: Alterar permissão de participante (não implementado)
- ⏳ **CDU-026**: Entrar em turma via código (não implementado)
- ⏳ **CDU-027**: Sair de turma (não implementado)
- ⏳ **CDU-028**: Atualizar preferências de turma (não implementado)

### 6.3 Resumo de Implementação

```
Total de CDUs: 29 (23 ativos, 2 removidos na v4)

✅ IMPLEMENTADOS:        CDU-001, 002, 003, 007, 009, 011, 017, 018, 020 (9)
⏳ PARCIALMENTE:         CDU-004, 005, 010, 012, 019 (5)
❌ NÃO IMPLEMENTADOS:    CDU-013, 014, 015, 016, 021, 022, 023, 024, 025, 026, 027, 028 (12)
~~REMOVIDOS:              CDU-008, CDU-029 (2)
```

**Taxa de Implementação: ~39% (9/23 CDUs)**

---

## 7. Partes Incompletas ou Não Implementadas

### 7.1 Resumo Crítico

| Componente | Status | Impacto | Detalhes |
|-----------|--------|--------|----------|
| **Perfil de Usuário** | ⏳ Vazio | Alto | Apenas renderiza template vazio |
| **Atualizar Dados de Usuário** | ❌ Não existe | Alto | CDU-005 não implementado |
| **Deletar Conta** | ❌ Não existe | Alto | CDU-006 não implementado |
| **Gerenciar Eventos** | ⏳ Crítico | Alto | Apenas criar parcial; faltam visualizar, editar, deletar |
| **Gerenciar Turma** | ⏳ Incompleto | Médio | Atualizar vazio; faltam operações com calendários |
| **Participantes de Turma** | ❌ Não existe | Alto | CDU-023 a CDU-028 não implementados |
| **Documentação BD** | ❌ Vazia | Médio | Apenas placeholders |
| **Documentação de Diagramas** | ⏳ Parcial | Médio | Diagramas UML não preenchidos |
| **Integração Calendário-Eventos** | ⏳ Vazia | Alto | Eventos não aparecem no calendário |

### 7.2 Detalhamento por App

#### **USUARIOS**
```python
❌ Atualizar conta (CDU-005)
   └─ Não existe view: /usuarios/editar/
   └─ Não existe template: usuarios/editar.html
   └─ Faltam campos editáveis

❌ Deletar conta (CDU-006)
   └─ Não existe view
   └─ Faltam validações de segurança

⏳ Perfil de usuário (CDU-004)
   └─ Arquivo vazio: usuarios/views/views.py (apenas 10 linhas)
   └─ Não renderiza dados do usuário
   └─ Sem funcionalidade real
```

#### **TURMAS**
```python
⏳ Atualizar turma (CDU-019)
   └─ views.py tem apenas: if membro.eh_admin: ...
   └─ Sem lógica implementada
   └─ Sem template

⏳ Adicionar calendário (CDU-021)
   └─ Não existe view ou template
   └─ Falta implementação completa

⏳ Remover calendário (CDU-022)
   └─ Não existe view ou template

❌ Gerenciar participantes (CDU-023 a CDU-028)
   └─ Nenhuma das 6 views implementada
   └─ Sem templates para estas operações
```

#### **CALENDARIOS**
```python
⏳ Atualizar calendário (CDU-010)
   └─ views.py tem apenas: if membro.eh_admin: ...
   └─ Sem lógica implementada
   └─ Sem template para edição
```

#### **EVENTOS**
```python
⏳ Criar evento (CDU-012)
   └─ Apenas view POST simples
   └─ Validações básicas
   └─ Sem interface visual integrada (apenas modal)

❌ Visualizar quadro geral (CDU-013)
   └─ Não existe view ou template
   └─ Deveria mostrar todos os eventos do usuário

❌ Visualizar evento individual (CDU-014)
   └─ Não existe view ou template

❌ Atualizar evento (CDU-015)
   └─ Não existe view ou template

❌ Deletar evento (CDU-016)
   └─ Não existe view ou template

⚠️  Integração calendário-eventos
   └─ Eventos existem no banco
   └─ Mas NÃO aparecem no calendário visual (inicio.html)
   └─ Calendário é estático (sem dados de eventos reais)
```

#### **CORE**
```python
✅ Página inicial com calendário semanal implementada
⏳ Mas calendário não exibe eventos do usuário
   └─ Deveria mostrar eventos dos calendários do usuário
   └─ Atualmente é apenas grid vazio de horas/dias
```

### 7.3 Problemas Técnicos Identificados

#### **1. Integração Calendário-Eventos** (CRÍTICO)
```
Problema: O calendário na página inicial não exibe os eventos
Causa: View inicio() não passa eventos para template
Impacto: Maior funcionalidade do app (visualizar prazos) não funciona

Código atual (core/views/inicio.py):
    context = {
        'dia_em_foco': dia_em_foco,
        'mes_em_foco': mes_em_foco,
        # ... SEM EVENTOS
    }
```

#### **2. Modais Desconectados**
```
Problema: Modais para criar eventos/turmas/calendários existem em teste_modal.html
Impacto: Interface para criação não está integrada nas páginas reais
Status: Apenas teste, não está em produção
```

#### **3. Views Vazias com Comentários**
```
Exemplos:
- turmas/views.py CDU-019: if membro.eh_admin: ...
- calendarios/views.py CDU-010: if membro.eh_admin: ...
- eventos/views.py: teste_modal() sem funcionalidade real
- usuarios/views/views.py: apenas 10 linhas
```

#### **4. Falta de Tratamento de Permissões**
```
Problema: Validações de permissões não são consistentes
Exemplo:
    - deletar_turma() valida admin
    - mas criar_evento() não valida calendário do usuário
    - visualizar_evento() não implementado (sem validação)
```

#### **5. Documentação de Banco de Dados**
```
Arquivo: doc/bd/bd.md
Status: Apenas template vazio
Faltam:
  ❌ Diagrama ER visual
  ❌ Modelo Relacional
  ❌ Dicionário de dados completo
  ❌ Scripts de criação do banco
```

### 7.4 Matriz de Completude do Projeto

```
┌─────────────────────────────────────────────────┐
│         ANÁLISE DE COMPLETUDE POR MÓDULO        │
├─────────────────────────────────────────────────┤
│                                                 │
│ AUTENTICAÇÃO       ████████░░░░░░░░░░░░░░░░░░  80%
│ USUÁRIOS           ████░░░░░░░░░░░░░░░░░░░░░░  20%
│ TURMAS             ██████░░░░░░░░░░░░░░░░░░░░  30%
│ CALENDÁRIOS        ██████░░░░░░░░░░░░░░░░░░░░  30%
│ EVENTOS            ███░░░░░░░░░░░░░░░░░░░░░░  15%
│ CORE               ████████░░░░░░░░░░░░░░░░░░  40%
│                                                 │
│ GERAL              ████░░░░░░░░░░░░░░░░░░░░░░  36%
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 8. Equipe e Contexto do Projeto

### 8.1 Equipe de Desenvolvimento

| Nome | E-mail | Função |
|------|--------|--------|
| André Isaque da Silva Lima | isaque.s@escolar.ifrn.edu.br | Desenvolvedor |
| Carlos Danilo Ramos dos Santos | carlos.danilo@escolar.ifrn.edu.br | Desenvolvedor |
| Giordanni Gomes Maciel | g.giordanni@escolar.ifrn.edu.br | Desenvolvedor |
| João Gabriel Figueiredo Feitosa | feitosa.joao@escolar.ifrn.edu.br | Desenvolvedor |
| Bianca Ferreira Dos Santos Teixeira | ??? | Desenvolvedor |

### 8.2 Repositório e Versionamento

- **Repositório**: GitHub (remoto: origin)
- **Branch Principal**: main
- **Workflow**: Feature branches com Pull Requests
- **Política de Commits**: Commits descritivos com issue numbers

### 8.3 Documentação Disponível

✅ [Documento de Visão](doc/visao/doc-visao.md) - v2.0 completo
✅ [Protótipos de Interface](doc/design/prototipos.md) - Disponível
✅ [Modelo de Casos de Uso](doc/cdu/cdu.md) - 23 CDUs ativos
✅ [Modelo de Domínio](doc/dominio/dominio.md) - Com diagrama UML
⏳ [Modelo de Dados](doc/bd/bd.md) - Apenas template
✅ [Guia do Desenvolvedor](doc/guia-ds/guia.md) - Completo

---

## 9. Recomendações e Próximos Passos

### 9.1 Prioridades Críticas (P0)

1. **Integrar Eventos no Calendário**
   - Modificar `core/views/inicio.py` para buscar eventos do usuário
   - Atualizar template `core/inicio.html` para renderizar eventos
   - Impacto: 🔴 Alto - é a funcionalidade central

2. **Completar Gerenciamento de Eventos**
   - Implementar views para: visualizar, atualizar, deletar (CDU-013, 014, 015, 016)
   - Criar templates correspondentes
   - Impacto: 🔴 Alto

3. **Completar Gerenciamento de Participantes de Turma**
   - Implementar CDU-023 a CDU-028
   - Falta a maior funcionalidade de colaboração
   - Impacto: 🔴 Alto

### 9.2 Prioridades Altas (P1)

4. **Completar CRUD de Usuários**
   - Perfil funcional (CDU-004)
   - Atualizar dados (CDU-005)
   - Deletar conta (CDU-006)

5. **Completar CRUD de Turmas/Calendários**
   - Atualizar turma (CDU-019)
   - Atualizar calendário (CDU-010)
   - Gerenciar calendários da turma (CDU-021, 022)

### 9.3 Prioridades Médias (P2)

6. **Documentação do Banco de Dados**
   - Completar Diagrama ER
   - Completar Modelo Relacional
   - Dicionário de Dados

7. **Testes Unitários e Integração**
   - Implementar testes para cada app
   - Cobertura de testes

### 9.4 Melhorias de UX/Design

8. **Integração de Modais**
   - Mover modais de teste_modal.html para páginas reais

9. **Implementação de Cores (Paleta)**
   - Sistema de paleta de cores não está implementado no frontend

---

## 10. Conclusão

O projeto **CAP - Calendário Acadêmico de Prazos** possui uma **arquitetura bem planejada e modelagem de dados sólida**, mas encontra-se em **fase inicial de implementação (~36% completo)**. 

### Pontos Positivos:
✅ Arquitetura modular bem estruturada
✅ Modelos Django bem definidos
✅ Documentação de requisitos completa
✅ Autenticação funcionando
✅ Estrutura de permissões e papéis

### Pontos Críticos:
❌ Integração calendário-eventos não funciona
❌ Maioria das operações CRUD incompleta
❌ Colaboração entre usuários não implementada
❌ Interface desconectada (modais em teste)
❌ Documentação BD vazia

### Recomendação:
Focar na conclusão das funcionalidades de **visualização e gerenciamento de eventos** (CDU-012 a 016), seguida da **integração com o calendário visual** e **gerenciamento de participantes de turma** (CDU-023 a 028), que são a essência da proposta de valor do projeto.

---

**Análise realizada em:** 13/08/2026
**Versão da análise:** 1.0
