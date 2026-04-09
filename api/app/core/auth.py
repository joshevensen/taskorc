import secrets

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db

_bearer = HTTPBearer(auto_error=False)


def generate_pat() -> str:
    return f"orc_{secrets.token_hex(32)}"


def hash_pat(pat: str) -> str:
    return bcrypt.hashpw(pat.encode(), bcrypt.gensalt()).decode()


def verify_pat(pat: str, pat_hash: str) -> bool:
    try:
        return bcrypt.checkpw(pat.encode(), pat_hash.encode())
    except Exception:
        return False


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = credentials.credentials

    # Import here to avoid circular imports at module load time
    from app.models.user import User

    result = await db.execute(select(User).where(User.pat_hash.is_not(None)))
    users = result.scalars().all()

    for user in users:
        if verify_pat(token, user.pat_hash):
            return user

    raise HTTPException(status_code=401, detail="Invalid token")
