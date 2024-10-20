# ASOS Backend

## Setup

### Install dependencies

#### With `uv`

```bash
cd backend && uv sync
```

#### With `pip`

Create a virtual environment and then run:

```bash
cd backend && pip install -r requirements
```

### Configure app using `.env`

```bash
cp .env.example .env
```

### Run migrations

```bash
alembic upgrade head
```

### Run api

```bash
uvicorn app.main:app
```

With hot-reloading:

```bash
uvicorn --reload app.main:app
```
