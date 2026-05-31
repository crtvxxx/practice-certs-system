from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend import schemas, models, auth
from backend.database import get_db
from sqlalchemy import select

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserOut)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.post("/register", response_model=schemas.UserOut)
async def register(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email уже используется")
    user = models.User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=auth.get_password_hash(user_data.password),
        role=user_data.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
async def login(login_data: schemas.LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.email == login_data.email))
    user = result.scalar_one_or_none()
    if not user or not auth.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}