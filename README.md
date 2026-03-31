# Tasks Domain API — Desafio Técnico Backend (Júnior)

API REST para gerenciamento de tasks, desenvolvida com FastAPI, SQLAlchemy e SQLite, com infraestrutura como código via Terraform + LocalStack.

---

## Tecnologias

- **Python 3.13.2** + **FastAPI**
- **SQLAlchemy** + **SQLite**
- **Pydantic** + **pydantic-settings**
- **PyJWT** + **pwdlib[argon2]**
- **Terraform** + **LocalStack**
- **Docker** + **Docker Compose**
- **Pytest** + **httpx**

---

## Estrutura do Projeto

```
tasks-domain/
├── app/
│   ├── requirements.txt
│   ├── settings.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_health.py
│   │   └── test_task_routes.py
│   └── src/
│       ├── main.py
│       ├── api/
│       │   └── routes/
│       │       ├── task.py
│       │       └── auth.py
│       ├── core/
│       │   ├── auth.py
│       │   └── exceptions.py
│       ├── db/
│       │   └── database.py
│       ├── models/
│       │   ├── task.py
│       │   └── user.py
│       ├── repositories/
│       │   ├── task_repository.py
│       │   └── user_repository.py
│       ├── schemas/
│       │   ├── task.py
│       │   └── user.py
│       └── services/
│           ├── task_service.py
│           └── auth_service.py
├── infra/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── providers.tf
│       └── inventories/
│           ├── local/
│           │   └── terraform.tfvars
│           ├── dev/
│           │   └── terraform.tfvars
│           ├── hom/
│           │   └── terraform.tfvars
│           └── prod/
│               └── terraform.tfvars
├── .env
├── docker-compose.yml
└── pytest.ini
```

---

A configuracao da aplicacao e centralizada em `app/settings.py`, responsavel por carregar variaveis via `.env` (como `DATABASE_URL`, `SECRET_KEY`, `JWT_ALGORITHM` e `ACCESS_TOKEN_EXPIRE_MINUTES`).

Os testes seguem organizacao por responsabilidade na pasta `app/tests`, com `conftest.py` para setup compartilhado e arquivos separados para rotas de health check e tasks. A execucao dos testes e padronizada por `pytest.ini` com `testpaths = app/tests`.

As models utilizam o padrao tipado do SQLAlchemy 2.x com `Mapped` e `mapped_column`, melhorando legibilidade e suporte de tipagem estatica.

---

## Endpoints

| Método   | Rota                        | Descrição                        |
|----------|-----------------------------|----------------------------------|
| `GET`    | `/health`                   | Healthcheck da aplicação         |
| `POST`   | `/auth/register`            | Cadastro de usuário              |
| `POST`   | `/auth/login`               | Login e geração de JWT           |
| `POST`   | `/tasks`                    | Criar uma task                   |
| `GET`    | `/tasks`                    | Listar todas as tasks            |
| `GET`    | `/tasks/{task_id}`          | Buscar uma task pelo ID          |
| `PATCH`  | `/tasks/{task_id}/status`   | Atualizar o status de uma task   |
| `DELETE`  | `/tasks/{task_id}`   | Exclui uma task   |

> As rotas de `tasks` são protegidas por JWT Bearer Token no header `Authorization`.

### Auth

**Cadastro (`POST /auth/register`):**

| Campo      | Tipo     | Obrigatório | Regras                       |
|------------|----------|-------------|------------------------------|
| `name`     | `string` | ✅           | Não vazio, máx. 255 caracteres |
| `email`    | `string` | ✅           | Não vazio, máx. 255 caracteres |
| `password` | `string` | ✅           | Mín. 6, máx. 100 caracteres    |

**Resposta:**

| Campo        | Tipo       |
|--------------|------------|
| `message`    | `string`   |
| `created_at` | `datetime` |

**Login (`POST /auth/login`):**

| Campo      | Tipo     | Obrigatório |
|------------|----------|-------------|
| `email`    | `string` | ✅           |
| `password` | `string` | ✅           |

**Resposta:**

| Campo          | Tipo     |
|----------------|----------|
| `access_token` | `string` |
| `token_type`   | `string` |

### Campos

**Criação (`POST /tasks`):**
| Campo         | Tipo     | Obrigatório | Regras                        |
|---------------|----------|-------------|-------------------------------|
| `title`       | `string` | ✅           | Não vazio, máx. 120 caracteres |
| `description` | `string` | ❌           | Máx. 1000 caracteres          |

**Resposta:**
| Campo         | Tipo       |
|---------------|------------|
| `id`          | `int`      |
| `title`       | `string`   |
| `description` | `string`   |
| `status`      | `string`   |
| `created_at`  | `datetime` |

**Status válidos:** `pending` · `in_progress` · `completed`

---

## Configuração Local

### 1. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 2. Instalar dependências

```bash
pip install -r app/requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=sua_chave_segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Executar a API

```bash
uvicorn src.main:app --reload --app-dir app
```

A API estará disponível em `http://localhost:8000`.
Documentação Swagger em `http://localhost:8000/docs`.

### 5. Executar os testes

```bash
pytest -q
```

---

## Infraestrutura (Terraform + LocalStack)

### 1. Iniciar o LocalStack

```bash
docker compose up -d
```

Aguarde o container ficar saudável:

```bash
curl http://localhost:4566/_localstack/health
```

### 2. Inicializar e aplicar o Terraform

```bash
cd infra/terraform

terraform init

terraform apply -var-file=inventories/local/terraform.tfvars
```

### 3. Recursos criados

- **DynamoDB Table** — `itau-junior-challenge-local-tasks`
- **S3 Bucket** — `itau-junior-challenge-local-uploads`
  - Lifecycle rule: `STANDARD → STANDARD_IA` (30 dias) `→ GLACIER` (90 dias) *(habilitado apenas em hom e prod)*

### Premissas por ambiente

| Ambiente | DynamoDB | S3  | Lifecycle S3 | Endpoint             |
|----------|----------|-----|--------------|----------------------|
| `local`  | ✅        | ✅  | ❌            | LocalStack (4566)    |
| `dev`    | ✅        | ❌  | ❌            | AWS (sa-east-1)      |
| `hom`    | ✅        | ✅  | ✅            | AWS (sa-east-1)      |
| `prod`   | ✅        | ✅  | ✅            | AWS (sa-east-1)      |

> Em `dev`, o S3 está desabilitado pois o ambiente serve apenas para validação funcional da API, sem necessidade de armazenamento de arquivos.

---

## Decisões do Candidato

### 1. Por que a camada de `service` foi usada

Decidi utilizar o service para isolar as regras de negócio do projeto, aplicando o princípio de responsabilidade única do SOLID. Isso permite que a camada de repositório seja substituída — por exemplo, trocar SQLite por PostgreSQL — sem tocar nas regras de negócio, e que os endpoints não precisem conhecer como os dados são persistidos.

### 2. Padrões de design aplicados

Utilizei o **Repository Pattern** para abstrair o acesso ao banco e uma **Service Layer** para centralizar as regras de negócio, resultando em camadas com responsabilidades bem definidas e fáceis de testar isoladamente.

### 3. Como os princípios SOLID foram considerados

- **SRP** — cada camada tem uma única responsabilidade: routes recebem e delegam, services aplicam regras, repositories acessam o banco
- **OCP** — novos endpoints podem ser adicionados sem modificar o service existente
- **DIP** — o service depende do repository via injeção, sem instanciar dependências diretamente

### 4. Principais trade-offs e o que seria melhorado com mais tempo

- **Lifecycle do S3 no LocalStack:** desabilitado no inventário `local` por limitação do LocalStack Community (free tier), que não suporta completamente esse recurso. Nos ambientes `hom` e `prod`, apontando para a AWS real, o `terraform apply` funcionaria sem problemas e a regra seria criada em segundos.

- **UUID vs Integer no ID:** optei por `Integer` autoincrement pela simplicidade com SQLite. Em produção, UUID seria mais adequado para evitar enumeração de recursos e facilitar distribuição em sistemas escaláveis.

- **Sem refresh token:** a autenticação JWT foi implementada para proteger os endpoints, mas sem rotação/refresh token neste momento.

- **CI/CD com GitHub Actions:** com mais tempo, adicionaria uma pipeline de CI/CD para execução automática dos testes e deploy da aplicação a cada Pull Request.

---

## Extras implementados

### Exceptions personalizadas

Além do escopo base do desafio, foi implementada uma camada de exceções personalizadas em `src/core/exceptions.py`, com hierarquia bem definida:

- `TaskException` — classe base
- `FailedToGetTaskException` — task não encontrada pelo ID
- `FailedToCreateTaskException` — falha na criação
- `FailedToUpdateTaskException` — falha na atualização de status
- `FailedToDeleteTaskException` — falha na exclusão
- `InvalidTaskStatusException` — status inválido fornecido
- `AuthException` — classe base para autenticação/autorização
- `AuthenticationFailedException` — falha genérica de autenticação
- `UserAlreadyExistsException` — tentativa de cadastro com e-mail já existente
- `UserNotFoundException` — usuário não encontrado
- `InvalidCredentialsException` — credenciais inválidas no login
- `TokenGenerationException` — falha ao gerar JWT
- `TokenValidationException` — token inválido ou expirado
- `AuthorizationException` — falha de autorização/acesso

Os handlers são registrados centralmente no `main.py` via `@app.exception_handler`, mantendo as rotas completamente limpas de blocos `try/except` e centralizando o tratamento de erros em um único lugar.

### Autenticação JWT

Também foi adicionada autenticação com JWT usando `PyJWT` e hash de senha com `pwdlib[argon2]`.

- Cadastro em `/auth/register`
- Login em `/auth/login` retornando `access_token`
- Proteção das rotas de `/tasks` com Bearer Token

### Método Delete e Patch

Também foi adicionado duas rotas a mais: `PATCH` e `DELETE`. Permitindo a atualização parcial e a exclusão de uma task.
