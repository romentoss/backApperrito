"""
🔐 Middleware de autenticación Firebase

Extrae y verifica el token de Firebase Auth del header Authorization.
Inyecta el user_id verificado en cada endpoint que lo necesite.

Uso en un router:
    @router.get("/")
    async def get_something(user_id: str = Depends(get_current_user_id)):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth

# HTTPBearer extrae automáticamente el token del header Authorization: Bearer <token>
bearer_scheme = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    """
    Verifica el token de Firebase Auth y retorna el user_id.
    Lanza 401 si el token es inválido o expirado.
    """
    token = credentials.credentials

    try:
        decoded = firebase_auth.verify_id_token(token)
        return decoded["uid"]
    except firebase_auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token de autenticación ha expirado.",
        )
    except firebase_auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación inválido.",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo verificar la autenticación.",
        )
