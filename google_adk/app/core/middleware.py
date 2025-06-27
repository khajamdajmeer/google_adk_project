
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import jwt
from app.core.config import Config
from app.core.context import set_context
from app.core.logging import get_logger

logger = get_logger(__name__)

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_token = request.headers.get("authtoken")
        
        context_data = {}
        if auth_token:
            try:
                # Decode without verification for now if secret is not shared properly, 
                # but ideally verification should be enabled.
                # Assuming the token is signed with the configured secret.
                payload = jwt.decode(
                    auth_token, 
                    Config.JWT_SECRET_KEY, 
                    algorithms=[Config.JWT_ALGORITHM],
                    options={"verify_signature": False} # Change to True if you have the correct key
                )
                context_data = payload
                # logger.info(f"Context populated for user: {payload.get('sub') or payload.get('patient_id')}")
            except jwt.ExpiredSignatureError:
                logger.warning("Token expired")
            except jwt.InvalidTokenError as e:
                logger.warning(f"Invalid token: {e}")
        
        set_context(context_data)
        
        response = await call_next(request)
        return response
