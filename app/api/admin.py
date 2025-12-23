from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.user import Token

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/backup")
async def trigger_backup(_ = Depends(RoleChecker([UserRole.ADMIN]))):
    file = create_db_backup()
    if file:
        remote_path = upload_to_remote(file)
        return {"status": "success", "path": remote_path}
    return {"status": "failed"}