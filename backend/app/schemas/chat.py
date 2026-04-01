"""
智能对话相关Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatMessageCreate(BaseModel):
    """创建对话消息"""
    message: str = Field(..., min_length=1)
    images: Optional[List[str]] = None
    session_id: Optional[str] = None
    diagnosis_context: Optional[dict] = None


class ChatAnnotation(BaseModel):
    """医疗术语标注"""
    term: str
    definition: str
    category: str


class RiskAssessment(BaseModel):
    """风险评估"""
    level: str
    factors: List[str]
    description: str


class ReferralSuggestion(BaseModel):
    """转诊建议"""
    suggested: bool
    reason: str
    urgency: str
    nearby_clinics: Optional[List[dict]] = None


class ChatReasoningStep(BaseModel):
    """推理步骤"""
    step: str
    content: str


class ChatMessageResponse(BaseModel):
    """对话消息响应"""
    id: int
    session_id: str
    
    role: str
    content: str
    images: Optional[List[str]] = None
    
    annotations: Optional[List[ChatAnnotation]] = None
    reasoning_steps: Optional[List[ChatReasoningStep]] = None
    
    risk_assessment: Optional[RiskAssessment] = None
    referral_suggestion: Optional[ReferralSuggestion] = None
    
    model_used: str
    processing_time: int
    
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    """对话响应"""
    reply: str
    session_id: str
    
    annotations: Optional[List[ChatAnnotation]] = None
    reasoning_steps: Optional[List[ChatReasoningStep]] = None
    
    risk_assessment: Optional[RiskAssessment] = None
    referral_suggestion: Optional[ReferralSuggestion] = None
    
    processing_time: int
    timestamp: datetime


class ChatSessionCreate(BaseModel):
    """创建对话会话"""
    title: Optional[str] = None


class ChatSessionResponse(BaseModel):
    """对话会话响应"""
    id: int
    session_id: str
    title: Optional[str] = None
    total_messages: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """对话历史响应"""
    session_id: str
    messages: List[ChatMessageResponse]
    total: int


class QuickQuestion(BaseModel):
    """快捷问题"""
    id: int
    question: str
    category: str


class QuickQuestionsResponse(BaseModel):
    """快捷问题列表响应"""
    questions: List[QuickQuestion]


class ClinicInfo(BaseModel):
    """诊所信息"""
    name: str
    address: str
    distance: float
    phone: str
    rating: Optional[float] = None
    hours: Optional[str] = None
