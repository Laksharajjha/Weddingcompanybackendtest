from pydantic import BaseModel, EmailStr, Field

class OrgCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., max_length=72)

class OrgUpdate(BaseModel):
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
