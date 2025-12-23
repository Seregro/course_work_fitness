from fastapi import APIRouter, Depends, Form, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models import User, Client, UserRole
from app.core.security import create_access_token

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(full_name: str=Form(...), email: str=Form(...), password: str=Form(...), db: AsyncSession=Depends(get_db)):
    user = User(email=email, hashed_password=password, full_name=full_name, role=UserRole.CLIENT)
    db.add(user)
    await db.flush()
    client = Client(user_id=user.id, phone="не указан", card_number=f"FIT-{user.id}")
    db.add(client)
    await db.commit()
    return RedirectResponse(url="/login", status_code=303)

@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_db)):
    print(f"DEBUG AUTH: Login attempt for {email}")
    res = await db.execute(select(User).where(User.email == email))
    user = res.scalar_one_or_none()

    if user and user.hashed_password == password:
        print("DEBUG AUTH: Password match! Setting cookie...")
        token = create_access_token({"sub": user.email})
        
        # Перенаправляем на главную
        resp = RedirectResponse(url="/", status_code=303)
        # Обязательно path="/", иначе кука будет работать только для /auth/
        resp.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, path="/")
        return resp
    
    print("DEBUG AUTH: Invalid credentials")
    return RedirectResponse(url="/login?error=1", status_code=303)

@router.get("/logout")
async def logout():
    resp = RedirectResponse(url="/login")
    resp.delete_cookie("access_token")
    return resp