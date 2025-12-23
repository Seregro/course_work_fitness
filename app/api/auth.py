from fastapi import APIRouter, Depends, HTTPException, status, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models import User, UserRole, Client
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register_user(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # 1. Проверяем, существует ли пользователь
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Создаем пользователя (User)
    new_user = User(
        email=email,
        hashed_password=get_password_hash(password),
        full_name=full_name,
        role=UserRole.CLIENT  # По умолчанию регистрируем как клиента
    )
    db.add(new_user)
    await db.flush()  # Получаем ID нового пользователя без коммита всей транзакции

    # 3. Создаем профиль клиента (Client)
    # Генерируем номер карты (упрощенно)
    card_num = f"FIT-{new_user.id:04d}"
    new_client = Client(
        user_id=new_user.id,
        phone=phone,
        card_number=card_num
    )
    db.add(new_client)
    
    await db.commit()
    return RedirectResponse(url="/login?registered=True", status_code=303)

@router.post("/login/html")
async def login_html(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    # Поиск пользователя
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        return RedirectResponse(url="/login?error=1", status_code=303)
    
    # Создаем токен (обязательно .value если это Enum)
    token = create_access_token(data={"sub": user.email, "role": user.role.value})
    
    # Выбираем куда идти
    if user.role == UserRole.ADMIN or user.role == UserRole.STAFF:
        target_url = "/admin/dashboard"
    else:
        target_url = "/me"

    response = RedirectResponse(url=target_url, status_code=303)
    
    # ВАЖНО: добавили path="/", чтобы кука была доступна везде
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token}", 
        httponly=True, 
        path="/", 
        samesite="lax"
    )
    print(f"DEBUG: User {user.email} logged in, redirecting to {target_url}")
    return response

@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response