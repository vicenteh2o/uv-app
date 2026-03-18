from fastapi import APIRouter, Response, status
from app.core.health import check_readiness

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Hello from uv 🚀"}


@router.get("/test")
def test_endpoint():
    return {"message": "This is a test endpoint"}


@router.get("/healthz")
async def liveness():
    """
    Liveness probe endpoint.

    Returns 200 if the process is running.
    This endpoint does not check database or external dependencies
    to avoid unnecessary pod restarts in Kubernetes.
    """
    return {"status": "alive"}


@router.get("/readyz")
async def readiness(response: Response):
    """
    Readiness probe endpoint.

    Returns 200 if all dependencies (database, external services) are available.
    Returns 503 if any dependency is unavailable, which will remove the pod
    from the load balancer until it recovers.
    """
    is_ready, details = await check_readiness()

    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return details
