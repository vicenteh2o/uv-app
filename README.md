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
