from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import generate_pat, get_current_user, hash_pat
from app.core.db import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenRequest(BaseModel):
    name: str
    email: str


@router.post("/token")
async def create_token(body: TokenRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(name=body.name, email=body.email)
        db.add(user)

    pat = generate_pat()
    user.pat_hash = hash_pat(pat)
    await db.commit()

    return {"token": pat, "note": "Store this token — it will not be shown again."}


@router.delete("/token")
async def revoke_token(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    current_user.pat_hash = None
    db.add(current_user)
    await db.commit()
    return {"message": "Token revoked. Run orc auth login to generate a new one."}
