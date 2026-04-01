"""数据库模型"""
from app.models.user import User, UserProfile, UserPermission
from app.models.diagnosis import DiagnosisRecord, DiagnosisResult
from app.models.chat import ChatSession, ChatMessage
from app.models.knowledge import DiseaseKnowledge, PreventionAdvice
