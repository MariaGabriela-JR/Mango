# RESTAPI - Cadastro e Gestão de Cientistas e Pacientes

Este documento descreve os endpoints, fluxos e uso da API Django RestAPI para registro, autenticação e gerenciamento de cientistas e pacientes.

---

## 1. Cadastro de Cientistas

- **Endpoint:** `POST /scientists/register/`
- **Descrição:** Cria um novo cientista no sistema.
- **Campos obrigatórios:**
  - `first_name`
  - `last_name`
  - `email` (único)
  - `password`
  - `institution`
  - `specialization`
- **Retorno:** JSON com dados do cientista registrado + **token JWT temporário (2 minutos)** para login inicial.

Exemplo de payload:
```json
{
  "first_name": "Ana",
  "last_name": "Silva",
  "email": "ana.silva@universidade.com",
  "password": "senha456",
  "institution": "Universidade Federal",
  "specialization": "Bioinformática"
}
```

Exemplo de resposta:
```json
{
  "id": "1a23bc45-67de-89f0-1234-56789abcde01",
  "email": "ana.silva@universidade.com",
  "first_name": "Ana",
  "last_name": "Silva",
  "institution": "Universidade Federal",
  "specialization": "Bioinformática",
  "registration_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 2. Login e Autenticação

- **Endpoint Cientistas:** `POST /auth/login/scientists/`
- **Endpoint Pacientes:** `POST /auth/login/patients/` *(apenas login, pacientes não se registram sozinhos)*
- **Retorno:** JSON com tokens JWT `access` e `refresh`.

Exemplo de resposta:
```json
{
  "access": "eyJhbGciOiJIUzI1...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## 3. Cadastro de Pacientes (via Cientista)

- **Endpoint:** `POST /patients/register/`
- **Descrição:** Cientista autenticado cria pacientes.
- **Requer:** Header `Authorization: Bearer <access> do cientista` e `X-Scientist-ID <id> do cientista`
- **Campos obrigatórios:**
  - `email` (único)
  - `password`
  - `first_name`
  - `last_name`
  - `age`
  - `gender`
- **Retorno:** JSON com dados do paciente registrado.

Exemplo de payload:
```json
{
  "id": "796d2b81-6c78-4bb8-b104-b4c0049b0ed6"
  "email": "paciente1@email.com",
  "password": "senha123",
  "first_name": "Marcos",
  "last_name": "Silva",
  "age": 21,
  "gender": "Masculino"
}
```

---

## 4. Listagem de Pacientes

- **Endpoint:** `GET /patients/list/`
- **Descrição:** Lista todos os pacientes cadastrados de um cientista.
- **Requer:** Cientista autenticado com headers `Authorization: Bearer <access> do cientista` e `X-Scientist-ID <id> do cientista`.
- **Retorno:** JSON com lista de pacientes:
  - `id` (UUID do paciente)
  - `email`
  - `scientist`
  - `first_name`
  - `last_name`
  - `age`
  - `gender`

Exemplo de resposta:
```json
[
  {
    "id": "796d2b81-6c78-4bb8-b104-b4c0049b0ed6",
    "email": "paciente1@email.com",
    "scientist": "1a23bc45-67de-89f0-1234-56789abcde01",
    "first_name": "Marcos",
    "last_name": "Silva",
    "age": 21,
    "gender": "Masculino"
  }
]
```

---

## 5. Detalhes do Usuário

- **Endpoint:** `GET /auth/me/`
- **Descrição:** Retorna informações do usuário autenticado.
- **Requer:** Header `Authorization: Bearer <token>`.

Exemplo de resposta:
```json
{
  "id": "1a23bc45-67de-89f0-1234-56789abcde01",
  "email": "ana.silva@universidade.com",
  "user_type": "scientist",
  "first_name": "Ana",
  "last_name": "Silva",
  "institution": "Universidade Federal",
  "specialization": "Bioinformática"
}
```

---

## 6. Logout

- **Endpoint:** `POST /auth/logout/`
- **Descrição:** Invalida o token de refresh.
- **Requer:** Token válido no corpo da requisição.

---

## 7. Resumo do Fluxo Completo

1. Cientista se registra (`/scientists/register/`) com **first_name, last_name, institution e specialization**. Recebe token temporário de 2 minutos.
2. Cientista faz login (`/auth/login/scientists/`) e recebe `access` + `refresh`.
3. Cientista cria pacientes (`/patients/register/`).
4. Cientista lista pacientes (`/patients/list/`).
5. Usuário valida sessão (`/auth/me/`).
6. Finaliza sessão (`/auth/logout/`).


