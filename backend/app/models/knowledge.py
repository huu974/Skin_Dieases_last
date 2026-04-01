"""
知识库模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float
from datetime import datetime
from app.core.database import Base


class DiseaseKnowledge(Base):
    """疾病知识库"""
    __tablename__ = "disease_knowledge"
    
    id = Column(Integer, primary_key=True, index=True)
    disease_name = Column(String(100), index=True)
    disease_name_en = Column(String(100))
    disease_code = Column(String(50))
    
    category = Column(String(50))
    severity = Column(String(20))
    contagion = Column(String(20))
    
    description = Column(Text)
    symptoms = Column(Text)
    causes = Column(Text)
    
    embedding = Column(JSON)
    
    season_prevalence = Column(JSON)
    age_group = Column(JSON)
    
    references = Column(JSON)
    
    is_published = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class PreventionAdvice(Base):
    """预防建议表"""
    __tablename__ = "prevention_advice"
    
    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer)
    disease_name = Column(String(100), index=True)
    
    prevention_tips = Column(JSON)
    dietary_advice = Column(JSON)
    nursing_advice = Column(JSON)
    
    seasonal_advice = Column(JSON)
    personalized_factors = Column(JSON)
    
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class SeasonalPush(Base):
    """季节性推送记录"""
    __tablename__ = "seasonal_push"
    
    id = Column(Integer, primary_key=True, index=True)
    season = Column(String(20))
    disease_name = Column(String(100))
    
    push_content = Column(Text)
    target_users = Column(JSON)
    
    is_sent = Column(Boolean, default=False)
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.now)
