FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY ./ ./
COPY .env.prod /app/.env

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

RUN alembic upgrade head

RUN python ./app/seed.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--root-path", "/api", "--proxy-headers"]
EXPOSE 8080
