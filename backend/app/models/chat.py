"""
智能对话模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ChatSession(Base):
    """对话会话表"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(50), unique=True, index=True)
    
    title = Column(String(200))
    context = Column(JSON)
    
    total_messages = Column(Integer, default=0)
    status = Column(String(20), default="active")
    
    created_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    """对话消息表"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    
    role = Column(String(20))
    content = Column(Text)
    images = Column(JSON)
    
    annotations = Column(JSON)
    reasoning_steps = Column(JSON)
    
    risk_assessment = Column(JSON)
    referral_suggestion = Column(JSON)
    
    model_used = Column(String(50))
    processing_time = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.now, index=True)
    
    session = relationship("ChatSession", back_populates="messages")
