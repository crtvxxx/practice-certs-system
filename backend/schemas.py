from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from backend.models import UserRole, CertificateType, OrderStatus

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.STUDENT

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: UserRole
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class OrderCreate(BaseModel):
    certificate_type: CertificateType
    reason: Optional[str] = ""

class OrderOut(BaseModel):
    id: int
    certificate_type: CertificateType
    reason: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    user: Optional[UserOut] = None
    model_config = {"from_attributes": True}