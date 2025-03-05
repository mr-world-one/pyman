#Third-party imports
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

#Local imports
from app.database import get_db
from app.models.model import User
from app.schemas.schema import UserCreate, UserResponse, User as UserSchema
from app.routers.authorization import get_password_hash

router = APIRouter()
logger = logging.getLogger(__name__)

# Створюємо юзера
@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Attempting to create user with email: {user.email}")
    try:
        # Check if user exists
        result = await db.execute(select(User).filter(User.email == user.email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        logger.info(f"Successfully created user with id: {db_user.id}")
        return db_user
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
# Отримання списку юзерів
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# Видалення юзера
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        await db.delete(user)
        await db.commit()
        return {"msg": "User deleted successfully"}
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to delete user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )