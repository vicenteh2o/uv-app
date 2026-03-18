# fastapi-uv-app

A minimal [FastAPI](https://fastapi.tiangolo.com/) application managed with [uv](https://github.com/astral-sh/uv), featuring linting, testing, and security scanning via pre-commit hooks.

---

## Requirements

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) installed

---

## Dependencies

### Runtime

| Package   | Version   | Purpose       |
| --------- | --------- | ------------- |
| `fastapi` | >=0.135.1 | Web framework |
| `uvicorn` | >=0.42.0  | ASGI server   |

### Dev

| Package         | Version  | Purpose                                     |
| --------------- | -------- | ------------------------------------------- |
| `httpx`         | >=0.28.1 | HTTP client for `TestClient` in tests       |
| `pytest`        | >=9.0.2  | Test runner                                 |
| `ruff`          | >=0.15.6 | Linter and formatter                        |
| `pre-commit`    | >=4.5.1  | Git hook manager                            |
| `pip-audit`     | >=2.10.0 | Dependency vulnerability scanner            |
| `cyclonedx-bom` | >=7.2.2  | Software Bill of Materials (SBOM) generator |

---

## Setup

```bash
uv sync --dev
uv run pre-commit install
```

---

## Running the app

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## Health Check Endpoints

The application includes two monitoring endpoints for Kubernetes liveness and readiness probes:

### `/healthz` (Liveness)

- Returns `200 OK` if the process is running
- Does not check database or external dependencies
- Use for Kubernetes `livenessProbe` to detect if the pod needs restart

```bash
curl http://localhost:8000/healthz
# Response: {"status":"alive"}
```

### `/readyz` (Readiness)

- Returns `200 OK` if all dependencies (database, external services) are available
- Returns `503 SERVICE UNAVAILABLE` if any dependency is down
- Use for Kubernetes `readinessProbe` to control load balancer traffic

```bash
curl http://localhost:8000/readyz
# Response: {"database":"healthy","status":"ready"}
```

### Next Steps

To integrate a real database check, update the `check_database()` function in `app/core/health.py`:

```python
# Example for PostgreSQL with asyncpg
async def check_database() -> bool:
    try:
        await db.execute("SELECT 1")
        return True
    except Exception:
        return False
```

Add external service checks in `check_external_services()` for Redis, message queues, APIs, etc.

---

## Testing

```bash
uv run pytest tests/ -v
```

---

## Docker

```bash
docker build -t fastapi-uv-app .
docker run -p 8000:8000 fastapi-uv-app
```

---

## Pre-commit hooks

Configured in [.pre-commit-config.yaml](.pre-commit-config.yaml). Runs automatically on every `git commit`.

| Hook             | Tool      | What it does                             |
| ---------------- | --------- | ---------------------------------------- |
| `ruff`           | ruff      | Lints the codebase and auto-fixes issues |
| `ruff-format`    | ruff      | Enforces consistent code formatting      |
| `pytest`         | pytest    | Runs the full test suite                 |
| `security-check` | pip-audit | Audits dependencies for known CVEs       |
