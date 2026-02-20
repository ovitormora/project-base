FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml .
RUN uv sync
COPY . /app
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "8000"]