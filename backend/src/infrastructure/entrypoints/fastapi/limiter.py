from slowapi import Limiter
from starlette.requests import Request

from src.config import settings
from src.shared.application.exceptions import TokenException
from src.shared.utils.auth.token_manager import JWTManager

_token_manager = JWTManager(settings)


def rate_limit_key(request: Request) -> str:
    """Key by user when a valid token is present, so that users sharing an IP
    (NAT, office, CGNAT) do not share a single bucket. Falls back to the IP."""
    try:
        token = request.headers.get("Authorization", "").removeprefix("Bearer ")
        return f"user:{_token_manager.get_username_from_token(token)}"
    except (TokenException, KeyError):
        client = request.client
        return f"ip:{client.host if client else 'unknown'}"


limiter = Limiter(
    key_func=rate_limit_key,
    storage_uri=settings.rate_limit_storage_uri,
    in_memory_fallback_enabled=True,
    key_style="endpoint",
)
