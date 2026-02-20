Aqui está o roteiro detalhado para a **Fase 1: Fundação & Ambiente de Desenvolvimento**. O objetivo desta fase é criar um alicerce sólido, automatizado e padronizado.

Vamos construir a estrutura de pastas, configurar os gestores de pacotes de alta performance (`uv` e `npm`), definir as regras de formatação de código e unir tudo com o Docker.

---

### Etapa 1: O Berço do Projeto

Vamos iniciar o repositório e criar a divisão clara entre o servidor (backend) e a interface (frontend).

**1. Comandos no Terminal:**

```bash
# Criação da pasta raiz do projeto
mkdir workout-api
cd workout-api

# Inicialização do repositório Git
git init

# Criação das pastas principais
mkdir backend frontend

# Criação de um ficheiro para ignorar ficheiros desnecessários no repositório
touch .gitignore

```

**2. Código (`.gitignore`):**

```text
# Node
node_modules/
dist/

# Python
__pycache__/
.venv/
.env

# SO
.DS_Store

```

**📌 Marco (Commit):**

```bash
git add .
git commit -m "chore: initialize project structure with backend and frontend folders"

```

*Mensagem do commit em inglês para manter o padrão profissional da indústria e praticar o idioma no dia a dia.*

---

### Etapa 2: Fundação do Backend (Python + uv)

Vamos configurar o ambiente Python de forma isolada, rápida e já com as ferramentas de qualidade de código.

**1. Comandos no Terminal:**

```bash
cd backend

# Inicializa o projeto Python com o uv
uv init

# Adiciona o FastAPI (framework) e o Ruff (linter/formatador)
uv add fastapi
uv add --dev ruff

# Cria a pasta da aplicação e o ficheiro principal
mkdir app
touch app/main.py

```

**2. Código (`backend/app/main.py`):**

```python
from fastapi import FastAPI

app = FastAPI(title="API Principal")

@app.get("/")
def read_root():
    return {"message": "Backend operante!"}

```

**3. Código (`backend/pyproject.toml` - O `uv init` cria este ficheiro, vamos apenas garantir que o Ruff está configurado no final dele):**

```toml
[project]
name = "backend"
version = "0.1.0"
dependencies = [
    "fastapi>=0.115.0",
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I"] # Ativa verificação de erros, falhas e ordenação de imports (I)

```

**📌 Marco (Commit):**

```bash
cd ..
git add backend/
git commit -m "chore(backend): setup python environment with uv, fastapi and ruff configuration"

```

---

### Etapa 3: Fundação do Frontend (React + npm)

Vamos criar a interface web utilizando as ferramentas no ecossistema JavaScript.

**1. Comandos no Terminal:**

```bash
cd frontend

# Cria o projeto React com TypeScript usando Vite e npm
npm create vite@latest . -- --template react-ts

# Instala as dependências base
npm install

# Instala o Biome (o nosso linter/formatador moderno para JS/TS)
npm install --save-dev @biomejs/biome

# Inicializa o ficheiro de configuração do Biome
npx @biomejs/biome init

```

**2. Código (`frontend/biome.json` - gerado automaticamente, mas ajustado para garantir formatação rigorosa):**

```json
{
  "$schema": "https://biomejs.dev/schemas/1.8.3/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  }
}

```

**📌 Marco (Commit):**

```bash
cd ..
git add frontend/
git commit -m "chore(frontend): bootstrap react-ts project with npm, vite and biome setup"

```

---

### Etapa 4: O "Segurança" da Qualidade (Pre-commit)

Para garantir que ninguém da equipa consegue guardar código mal formatado ou com erros no Git.

**1. Comandos no Terminal:**

```bash
# Na pasta raiz (workout-api)
touch .pre-commit-config.yaml

```

**2. Código (`.pre-commit-config.yaml`):**

```yaml
repos:
  # Formatação e Linting do Backend (Python)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [ --fix ]
      - id: ruff-format

  # Formatação e Linting do Frontend (JS/TS)
  - repo: https://github.com/biomejs/pre-commit
    rev: v0.1.0
    hooks:
      - id: biome-check
        additional_dependencies: ["@biomejs/biome@1.8.3"]

```

**📌 Marco (Commit):**

```bash
git add .pre-commit-config.yaml
git commit -m "ci: add pre-commit hooks to enforce ruff (python) and biome (typescript) formatting"

```

---

### Etapa 5: O Maestro da Infraestrutura (Docker Compose)

Vamos orquestrar o backend e o frontend para rodarem juntos com um único comando, simulando o ambiente de produção, mas com *live reload* para desenvolvimento.

**1. Comandos no Terminal:**

```bash
# Na pasta raiz
touch compose.yml compose.override.yml backend/Dockerfile frontend/Dockerfile

```

**2. Código (`backend/Dockerfile`):**

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml .
RUN uv sync
COPY . /app
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "8000"]

```

**3. Código (`frontend/Dockerfile`):**

```dockerfile
FROM node:20-slim AS base
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

```

**4. Código (`compose.yml` - A Base da Infraestrutura):**

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000

```

**5. Código (`compose.override.yml` - O segredo para o desenvolvimento local fluído):**

```yaml
services:
  backend:
    # Espelha a pasta local dentro do contentor para não precisar de reconstruir a imagem
    volumes:
      - ./backend:/app
    # Executa a API no modo "dev" (live reload ativo)
    command: uv run fastapi dev app/main.py --host 0.0.0.0

  frontend:
    volumes:
      - ./frontend:/app
      - /app/node_modules # Impede que o node_modules local sobrescreva o do contentor

```

**📌 Marco Final (Commit):**

```bash
git add .
git commit -m "feat: implement docker compose architecture with hot-reload for local development"

```

A partir deste momento, basta digitar `docker compose watch` (ou `docker compose up --build`) na raiz do projeto. O backend estará disponível na porta 8000 e o frontend na porta 5173, ambos ligados e a atualizar em tempo real à medida que escreve o código. A Fase 1 está concluída e blindada!