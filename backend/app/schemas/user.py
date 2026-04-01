"""
用户相关Schema
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    USER = "user"
    VISITOR = "visitor"


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str = Field(..., min_length=6)
    role: UserRoleEnum = UserRoleEnum.USER


class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = None
    skin_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = None
    skin_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    preferences: Optional[dict] = None
    privacy_settings: Optional[dict] = None


class PrivacySettingsUpdate(BaseModel):
    data_encryption_enabled: Optional[bool] = None
    data_sharing_enabled: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    skin_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class VisitorRegisterResponse(BaseModel):
    visitor_id: str
    session_token: str
    expires_in: int
