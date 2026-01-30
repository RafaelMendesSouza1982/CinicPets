# 🐾 Documentação Técnica – Sistema de Gestão para Petshop (Python)

## 1. Visão Geral do Sistema

O **Sistema de Gestão para Petshop** é uma aplicação web desenvolvida em **Python**, voltada para clínicas veterinárias e petshops, com foco em organização de atendimentos, prontuário animal e agenda diária.

O sistema é dividido em:

* **Área interna (restrita por autenticação)**: gestão completa do petshop
* **Área externa (pública)**: visualização da agenda de atendimentos do dia

A solução utiliza arquitetura moderna, APIs REST e ambiente totalmente **containerizado com Docker**.

---

## 2. Objetivos do Sistema

* Centralizar cadastro de responsáveis, animais e veterinários
* Gerenciar consultas e atendimentos clínicos
* Registrar medicações e histórico veterinário
* Disponibilizar agenda pública diária
* Garantir segurança, rastreabilidade e escalabilidade

---

## 3. Tecnologias Utilizadas

### Backend

* Python 3.11+
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic (migrations)

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript (ES6+)
* Jinja2 (templates)

### Banco de Dados

* PostgreSQL 14+

### Infraestrutura

* Docker
* Docker Compose
* Nginx (Reverse Proxy)

---

## 4. Arquitetura do Sistema

### 4.1 Padrão Arquitetural

* Arquitetura em camadas
* API REST
* Separação entre frontend e backend

### 4.2 Containers Docker

| Container         | Função                     |
| ----------------- | -------------------------- |
| api               | FastAPI (backend)          |
| worker (opcional) | Processamentos assíncronos |
| db                | PostgreSQL                 |
| web               | Nginx + Frontend           |

---

## 5. Perfis de Usuário

### Administrador

* Gerencia usuários
* Cadastro de veterinários
* Acesso total

### Veterinário

* Visualiza agenda
* Registra atendimentos
* Prescreve medicações

### Recepção

* Cadastra responsáveis
* Cadastra animais
* Agenda consultas

---

## 6. Módulos do Sistema

### 6.1 Autenticação

* Login com e-mail e senha
* Autenticação JWT
* Controle de acesso por perfil

---

### 6.2 Cadastro de Responsável (Cliente)

**Campos:**

* Nome
* CPF
* Telefone
* E-mail
* Endereço

Regras:

* CPF único
* Um responsável pode possuir vários animais

---

### 6.3 Cadastro de Animais

**Campos:**

* Nome
* Espécie
* Raça
* Sexo
* Data de nascimento
* Responsável vinculado

---

### 6.4 Cadastro de Veterinários

**Campos:**

* Nome
* CRMV
* Especialidade
* Contato

Regras:

* CRMV único

---

### 6.5 Marcação de Consultas

**Dados:**

* Animal
* Veterinário
* Data
* Horário
* Tipo de atendimento

Regras:

* Não permitir conflito de horário para o mesmo veterinário
* Consulta deve estar associada a um animal válido

---

### 6.6 Atendimento Clínico

Durante o atendimento o veterinário pode:

* Registrar observações clínicas
* Informar diagnóstico
* Registrar procedimentos

---

### 6.7 Medicação

**Campos:**

* Nome do medicamento
* Dosagem
* Frequência
* Duração

Regras:

* Medicação vinculada a um atendimento

---

### 6.8 Histórico de Atendimento

* Histórico completo por animal
* Consultas anteriores
* Diagnósticos
* Medicações prescritas

---

## 7. Área Externa – Agenda Pública

### Funcionalidade

* Exibição da agenda do dia
* Lista de atendimentos por horário

### Informações exibidas

* Horário
* Nome do animal
* Tipo de atendimento

### Restrições

* Não exibir dados do responsável
* Não requer autenticação

---

## 8. Modelagem de Dados (Principais Entidades)

### Users

* id
* nome
* email
* senha_hash
* perfil

### Responsaveis

* id
* nome
* cpf
* telefone
* email
* endereco

### Animais

* id
* nome
* especie
* raca
* sexo
* data_nascimento
* responsavel_id

### Veterinarios

* id
* nome
* crmv
* especialidade

### Consultas

* id
* animal_id
* veterinario_id
* data
* horario
* status

### Atendimentos

* id
* consulta_id
* observacoes
* diagnostico

### Medicacoes

* id
* atendimento_id
* medicamento
* dosagem
* frequencia
* duracao

---

## 9. Regras de Negócio

### RN01 – Autenticação

* Apenas usuários autenticados acessam a área interna

### RN02 – Agenda

* Veterinário não pode ter duas consultas no mesmo horário

### RN03 – Histórico Clínico

* Histórico não pode ser excluído

### RN04 – Integridade de Dados

* Responsável não pode ser removido se possuir animais ativos

---

## 10. Fluxo de Uso do Sistema

1. Usuário realiza login
2. Recepção cadastra responsável e animal
3. Consulta é agendada
4. Veterinário realiza atendimento
5. Medicação é registrada
6. Histórico é armazenado
7. Agenda pública exibe atendimentos do dia

---

## 11. Segurança e Boas Práticas

* Senhas criptografadas
* JWT com expiração
* Proteção contra SQL Injection
* Validação de dados via Pydantic

---

## 12. Evoluções Futuras

* Agendamento online pelo cliente
* Notificações por WhatsApp e e-mail
* Prontuário eletrônico avançado
* Controle financeiro e faturamento

---

📌 **Documento técnico para desenvolvimento de sistemas veterinários modernos em Python.**
