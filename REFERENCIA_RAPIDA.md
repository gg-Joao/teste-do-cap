# 🗂️ REFERÊNCIA RÁPIDA - Estrutura do Projeto CAP

## Navegação por Componente

### 📚 Documentação
| Arquivo | Localização | Assunto |
|---------|-------------|---------|
| Visão Geral | `/doc/visao/doc-visao.md` | Requisitos, usuários, RN |
| Casos de Uso | `/doc/cdu/cdu.md` | Lista de 29 CDUs |
| Diagrama UML | `/doc/cdu/diagramas/` | Diagramas de arquitetura |
| Banco de Dados | `/doc/bd/bd.md` | ER, MR, Dicionário (VAZIO) |
| Design | `/doc/design/prototipos.md` | Wireframes e UI |
| Guia Dev | `/doc/guia-ds/guia.md` | Workflow Git, padrões |
| Domínio | `/doc/dominio/dominio.md` | Modelo de classes |

---

## 🏗️ Backend (Django)

### Estrutura de Arquivos
```
mysite/
├── apps/
│   ├── usuarios/
│   │   ├── models/
│   │   │   ├── usuario.py          [CORE]
│   │   │   └── usuario_manager.py
│   │   ├── views/
│   │   │   ├── autenticacao.py     ✅ Login/Logout/Cadastro
│   │   │   └── views.py            ⏳ Perfil vazio
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── templates/
│   │       ├── login.html          ✅
│   │       ├── cadastro.html       ✅
│   │       └── perfil.html         ⏳
│   │
│   ├── turmas/
│   │   ├── models/
│   │   │   ├── turma.py            ✅ Modelo completo
│   │   │   └── membro_de_turma.py  ✅
│   │   ├── views.py                ⚠️ Parcial
│   │   ├── urls.py
│   │   └── templates/
│   │       └── turma.html          ✅
│   │
│   ├── calendarios/
│   │   ├── models/
│   │   │   ├── calendario.py       ✅ Modelo completo
│   │   │   └── membro_de_calendario.py ✅
│   │   ├── views.py                ⚠️ Parcial
│   │   ├── urls.py
│   │   └── templates/
│   │       └── calendario.html     ✅
│   │
│   ├── eventos/
│   │   ├── models/
│   │   │   └── evento.py           ✅ Modelo completo
│   │   ├── views.py                ⏳ Crítico
│   │   ├── urls.py
│   │   ├── calendarios_context.py  (não documentado)
│   │   └── templates/
│   │       ├── modal_criar_evento.html
│   │       ├── modal_editar_evento.html
│   │       ├── modal_vizualizar_evento.html
│   │       └── teste_modal.html
│   │
│   └── core/
│       ├── models/
│       │   └── base_model.py       ✅ Superclasse abstrata
│       ├── views/
│       │   ├── inicio.py           ✅ Calendário semanal
│       │   ├── menu_lateral.py
│       │   └── views.py            (vazio)
│       ├── urls.py
│       ├── context_processors.py
│       ├── management/commands/
│       │   ├── populate.py
│       │   └── dados_populate.py
│       └── templates/
│           ├── base.html           ✅ Template base
│           ├── inicio.html         ✅ Página inicial
│           └── menu_lateral.html   ✅
│
└── config/
    ├── settings/
    │   ├── settings.py
    │   ├── development.py
    │   ├── production.py
    │   └── testing.py
    ├── urls.py                     ✅ Roteamento principal
    ├── wsgi.py
    └── asgi.py
```

---

## 🔑 Modelos Principais

### Usuario
```python
# apps/usuarios/models/usuario.py
class Usuario(BaseModel, AbstractBaseUser, PermissionsMixin):
    email (unique)
    nome_completo
    is_active
    is_staff
    
    Métodos:
    - paleta_menos_usada()
    - primeiro_nome()
```

### Turma
```python
# apps/turmas/models/turma.py
class Turma(BaseModel):
    nome
    descricao
    codigo (unique, auto-gerado)
    usuarios (M2M via MembroDeTurma)
```

### MembroDeTurma
```python
# apps/turmas/models/membro_de_turma.py
class MembroDeTurma(BaseModel):
    usuario (FK)
    turma (FK)
    eh_admin (Boolean)
    numero_paleta (0-9)
    Constraint: unique(usuario, turma)
```

### Calendario
```python
# apps/calendarios/models/calendario.py
class Calendario(BaseModel):
    nome
    descricao
    turma (FK, nullable - para calendários pessoais)
    usuarios (M2M via MembroDeCalendario)
```

### MembroDeCalendario
```python
# apps/calendarios/models/membro_de_calendario.py
class MembroDeCalendario(BaseModel):
    usuario (FK)
    calendario (FK)
    eh_admin (Boolean)
    numero_paleta (0-9)
    Constraint: unique(usuario, calendario)
```

### Evento
```python
# apps/eventos/models/evento.py
class Evento(BaseModel):
    nome
    conteudo
    inicio (DateTime, validado 2000-2050)
    fim (DateTime, validado 2000-2050)
    calendario (FK)
    
    Validações:
    - mesmo dia início e fim
    - fim > início
```

### BaseModel (Superclasse)
```python
# apps/core/models/base_model.py
class BaseModel(models.Model):
    criado_em (auto_now_add)
    alterado_em (auto_now)
    # Herança abstrata
```

---

## 🛣️ Roteamento de URLs

### Principais Rotas
```python
# config/urls.py
'' → apps.core.urls         [Página inicial]
'usuarios/' → apps.usuarios.urls
'turmas/' → apps.turmas.urls
'calendarios/' → apps.calendarios.urls
'eventos/' → apps.eventos.urls
'admin/' → Django admin
```

### Rotas Implementadas
#### Autenticação (CORE)
- `POST /usuarios/login/` → login_view
- `GET /usuarios/logout/` → logout_view
- `GET /` → inicio (requer login)

#### Turmas
- `GET /turmas/{id}/` → turma
- `GET /turmas/criar/` → criar_turma
- `POST /turmas/{id}/atualizar/` → atualizar_turma
- `GET /turmas/{id}/deletar/` → deletar_turma

#### Calendários
- `GET /calendarios/{id}/` → calendario
- `GET /calendarios/criar/` → criar_calendario
- `POST /calendarios/{id}/atualizar/` → atualizar_calendario
- `GET /calendarios/{id}/deletar/` → deletar_calendario

#### Eventos
- `POST /eventos/criar/` → criar_evento
- `GET /eventos/teste/` → teste_modal

---

## 📊 Matriz de CDU vs Implementação

### Autenticação
| CDU | Nome | Status | View | Template |
|-----|------|--------|------|----------|
| 001 | Entrar | ✅ | autenticacao.py | login.html |
| 002 | Sair | ✅ | autenticacao.py | N/A |

### Conta
| CDU | Nome | Status | View | Template |
|-----|------|--------|------|----------|
| 003 | Criar | ✅ | autenticacao.py | cadastro.html |
| 004 | Visualizar | ⏳ | views.py | perfil.html |
| 005 | Atualizar | ❌ | ❌ | ❌ |
| 006 | Deletar | ❌ | ❌ | ❌ |

### Calendários
| CDU | Nome | Status | View | Template |
|-----|------|--------|------|----------|
| 007 | Criar | ✅ | views.py | N/A |
| 009 | Visualizar | ✅ | views.py | calendario.html |
| 010 | Atualizar | ⏳ | views.py (vazio) | ❌ |
| 011 | Deletar | ✅ | views.py | N/A |

### Eventos
| CDU | Nome | Status | View | Template |
|-----|------|--------|------|----------|
| 012 | Criar | ⏳ | views.py (parcial) | modal_criar_evento.html |
| 013 | Quadro Geral | ❌ | ❌ | ❌ |
| 014 | Visualizar | ❌ | ❌ | modal_vizualizar_evento.html |
| 015 | Atualizar | ❌ | ❌ | modal_editar_evento.html |
| 016 | Deletar | ❌ | ❌ | ❌ |

### Turmas
| CDU | Nome | Status | View | Template |
|-----|------|--------|------|----------|
| 017 | Criar | ✅ | views.py | N/A |
| 018 | Visualizar | ✅ | views.py | turma.html |
| 019 | Atualizar | ⏳ | views.py (vazio) | ❌ |
| 020 | Deletar | ✅ | views.py | N/A |
| 021 | Adicionar Cal | ❌ | ❌ | ❌ |
| 022 | Remover Cal | ❌ | ❌ | ❌ |

### Participação em Turmas
| CDU | Nome | Status | View | Template |
|-----|------|--------|------|----------|
| 023 | Consultar Partic | ❌ | ❌ | ❌ |
| 024 | Remover Partic | ❌ | ❌ | ❌ |
| 025 | Alterar Permissão | ❌ | ❌ | ❌ |
| 026 | Entrar Turma | ❌ | ❌ | ❌ |
| 027 | Sair Turma | ❌ | ❌ | ❌ |
| 028 | Atualizar Pref | ❌ | ❌ | ❌ |

---

## 🎨 Templates Criados

### Autenticação
- ✅ usuarios/login.html
- ✅ usuarios/cadastro.html

### Usuários
- ⏳ usuarios/perfil.html (vazio)

### Turmas
- ✅ turmas/turma.html

### Calendários
- ✅ calendarios/calendario.html

### Eventos
- ⏳ eventos/modal_criar_evento.html
- ⏳ eventos/modal_editar_evento.html
- ⏳ eventos/modal_vizualizar_evento.html
- ⏳ eventos/teste_modal.html (desconectado)

### Core/Layout
- ✅ core/base.html (template base)
- ✅ core/inicio.html (página inicial)
- ✅ core/menu_lateral.html

---

## 🔴 Pontos Críticos Agora

1. **Eventos não aparecem no calendário** (core/inicio.html)
   - `context` em `views/inicio.py` não contém eventos
   - Template não renderiza eventos

2. **CDU-013 a CDU-016 não existem**
   - Faltam views para gerenciar eventos

3. **CDU-023 a CDU-028 não existem**
   - Colaboração entre usuários não funciona

4. **Views vazias**
   - usuarios/views/views.py
   - turmas/views.py - if membro.eh_admin: ...
   - calendarios/views.py - if membro.eh_admin: ...

---

## 📦 Dependências

```
asgiref==3.11.1          (ASGI server)
Django==6.0.6            (Framework)
pillow==12.2.0           (Imagens)
sqlparse==0.5.5          (Parsing SQL)
tzdata==2026.2           (Timezones)
```

---

## 🚀 Como Começar

### Clonar e Setup
```bash
git clone https://github.com/tads-cnat/2026-CAP.git
cd 2026-CAP-main
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd mysite
python manage.py migrate
python manage.py runserver
```

### Acessar
- Página inicial: http://localhost:8000/
- Admin: http://localhost:8000/admin/

---

## 📋 Checklist de Próximas Ações

- [ ] Integrar eventos no calendário visual
- [ ] Completar CRUD eventos (CDU-012-016)
- [ ] Implementar gerenciamento participantes (CDU-023-028)
- [ ] Completar CRUD usuários (CDU-004-006)
- [ ] Completar operações de UPDATE
- [ ] Preencher documentação BD
- [ ] Adicionar testes
- [ ] Implementar sistema de cores

---

**Última atualização:** 13/08/2026
