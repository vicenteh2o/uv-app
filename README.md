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

---

## Contributing — PR merge strategy

This project uses [`python-semantic-release`](https://python-semantic-release.readthedocs.io/) v10 to automate version bumping and changelog generation. It reads commit messages on `main` and applies [Conventional Commits](https://www.conventionalcommits.org/) rules to decide the next version.

### ⚠️ Always use **Squash and merge**

When merging a Pull Request, **always select "Squash and merge"** in the GitHub UI. This ensures the PR title (which must follow Conventional Commits format) becomes the single commit message on `main`.

Examples of valid PR titles:

| Type | Example PR title | Effect |
| ---- | ---------------- | ------ |
| New feature | `feat: add user authentication` | bumps **minor** version |
| Bug fix | `fix: correct null pointer in health check` | bumps **patch** version |
| Breaking change | `feat!: redesign API response format` | bumps **major** version |
| Docs / chores | `docs: update README` / `chore: bump deps` | no version bump (excluded) |

> **Why not "Create a merge commit"?**
> GitHub's default merge commit message is `Merge pull request #N from owner/branch`, which is not a Conventional Commit and will be ignored by semantic-release — no new version will be generated.

> **Why not "Rebase and merge"?**
> This works only if **every individual commit** on the branch follows Conventional Commits. Squash and merge is simpler and less error-prone.

### Enforcing squash merges via repository settings

Repository admins can enforce squash-only merges:
1. Go to **Settings → General → Pull Requests**.
2. Uncheck **Allow merge commits** and **Allow rebase merging**.
3. Keep only **Allow squash merging** checked and set the default commit message to **Pull request title**.

### Initial base tag

`python-semantic-release` requires a base git tag to calculate the next version. The initial tag `v0.1.0` must exist on `main`. If it is missing, create it manually:

```bash
# Tag the current HEAD of main (replace <sha> with the actual commit SHA if needed)
git tag v0.1.0
git push origin v0.1.0
```
