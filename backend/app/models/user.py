"""
用户模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class UserRole(enum.Enum):
    """用户角色"""
    ADMIN = "admin"
    DOCTOR = "doctor"
    USER = "user"
    VISITOR = "visitor"


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    data_encryption_enabled = Column(Boolean, default=True)
    data_sharing_enabled = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_login = Column(DateTime)
    
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    diagnoses = relationship("DiagnosisRecord", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")


class UserProfile(Base):
    """用户详细信息表"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    name = Column(String(50))
    age = Column(Integer)
    gender = Column(String(10))
    skin_type = Column(String(20))
    allergies = Column(Text)
    medical_history = Column(Text)
    
    address = Column(String(200))
    emergency_contact = Column(String(50))
    emergency_phone = Column(String(20))
    
    preferences = Column(JSON)
    privacy_settings = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship("User", back_populates="profile")


class UserPermission(Base):
    """用户权限表"""
    __tablename__ = "user_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    can_use_ai_diagnosis = Column(Boolean, default=True)
    can_use_chat = Column(Boolean, default=True)
    can_view_history = Column(Boolean, default=True)
    can_export_data = Column(Boolean, default=True)
    can_share_data = Column(Boolean, default=False)
    
    diagnosis_quota = Column(Integer, default=100)
    chat_quota = Column(Integer, default=1000)
    
    created_at = Column(DateTime, default=datetime.now)


from sqlalchemy import ForeignKey
