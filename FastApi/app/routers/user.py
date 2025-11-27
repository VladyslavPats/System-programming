from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.dependencies import get_session
from app.core.models.user import User
from app.core.schemas.user import UserCreateSchema, UserResponseSchema, UserPartialUpdateSchema

router = APIRouter(
    prefix="/users",
    tags=["Users Management"]
)

@router.post("/", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    new_user = User(email=user_data.email, password_hash=user_data.password, role=user_data.role)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserResponseSchema])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    result = await session.scalars(select(User))
    return result.all()

@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з ID {user_id} не знайдено.")
    return user

@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_full_user(user_id: int, user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з ID {user_id} не знайдено.")
    user.email = user_data.email
    user.password_hash = user_data.password
    user.role = user_data.role
    await session.commit()
    await session.refresh(user)
    return user

@router.patch("/{user_id}", response_model=UserResponseSchema)
async def update_partial_user(user_id: int, user_data: UserPartialUpdateSchema, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з ID {user_id} не знайдено.")
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "password":
            setattr(user, "password_hash", value)
        else:
            setattr(user, field, value)
    await session.commit()
    await session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з ID {user_id} не знайдено.")
    await session.delete(user)
    await session.commit()
    return