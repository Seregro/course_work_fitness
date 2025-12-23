    
from fastapi import Request, Depends
from jose import jwt
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import get_db
from app.models import User
from sqlalchemy import select

async def get_current_user(request: Request, db = Depends(get_db)):
    token = request.cookies.get("access_token")
    
    if not token:
        print("DEBUG DEPS: No cookie found")
        return None
    
    try:
        # Убираем Bearer
        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if user:
            print(f"DEBUG DEPS: User found: {user.email}")
            return user
        
        print("DEBUG DEPS: User not in database")
        return None
    except Exception as e:
        print(f"DEBUG DEPS: JWT Decode error: {e}")
        return None

  