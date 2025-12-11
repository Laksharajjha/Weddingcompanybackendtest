from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.payload import UserLogin, TokenResponse
from app.db.database import db
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/admin/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    user = await db.get_db()["users"].find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
