# Tasks Domain API — Desafio Técnico Backend (Júnior)

API REST para gerenciamento de tasks, desenvolvida com FastAPI, SQLAlchemy e SQLite, com infraestrutura como código via Terraform + LocalStack.

---

## Tecnologias

- **Python** + **FastAPI**
- **SQLAlchemy** + **SQLite**
- **Pydantic** + **pydantic-settings**
- **Terraform** + **LocalStack**
- **Docker** + **Docker Compose**
- **Pytest** + **httpx**

---

## Estrutura do Projeto

```
tasks-domain/
├── app/
│   ├── requirements.txt
│   └── src/
│       ├── main.py
│       ├── api/
│       │   └── routes/
│       │       └── task.py
│       ├── core/
│       │   ├── config.py
│       │   └── exceptions.py
│       ├── db/
│       │   └── database.py
│       ├── models/
│       │   └── task.py
│       ├── repositories/
│       │   └── task_repository.py
│       ├── schemas/
│       │   └── task.py
│       └── services/
│           └── task_service.py
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

## Endpoints

| Método   | Rota                        | Descrição                        |
|----------|-----------------------------|----------------------------------|
| `GET`    | `/health`                   | Healthcheck da aplicação         |
| `POST`   | `/tasks`                    | Criar uma task                   |
| `GET`    | `/tasks`                    | Listar todas as tasks            |
| `GET`    | `/tasks/{task_id}`          | Buscar uma task pelo ID          |
| `PATCH`  | `/tasks/{task_id}/status`   | Atualizar o status de uma task   |
| `DELETE`  | `/tasks/{task_id}`   | Exclui uma task   |

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
```

### 4. Executar a API

```bash
uvicorn src.main:app --reload --app-dir app
```

A API estará disponível em `http://localhost:8000`.
Documentação Swagger em `http://localhost:8000/docs`.

### 5. Executar os testes

```bash
pytest app/tests -q
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

- **Sem autenticação:** a API não possui autenticação. Com mais tempo, adicionaria JWT ou API Key para proteger os endpoints.

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

Os handlers são registrados centralmente no `main.py` via `@app.exception_handler`, mantendo as rotas completamente limpas de blocos `try/except` e centralizando o tratamento de erros em um único lugar.

### Método Delete e Patch

Também foi adicionado duas rotas a mais: `PATCH` e `DELETE`. Permitindo a atualização parcial e a exclusão de uma task.
