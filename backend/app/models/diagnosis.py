"""
诊断记录模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class DiagnosisRecord(Base):
    """诊断记录表"""
    __tablename__ = "diagnosis_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(50), index=True)
    
    image_path = Column(String(500))
    image_hash = Column(String(64))
    
    models_used = Column(JSON)
    diagnosis_mode = Column(String(20))
    
    detection_result = Column(JSON)
    classification_result = Column(JSON)
    
    primary_disease = Column(String(100))
    primary_confidence = Column(Float)
    all_results = Column(JSON)
    
    lesion_coordinates = Column(JSON)
    
    risk_level = Column(String(20))
    recommendation = Column(Text)
    
    pdf_report_path = Column(String(500))
    
    is_shared = Column(Boolean, default=False)
    is_anonymous = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship("User", back_populates="diagnoses")
    results = relationship("DiagnosisResult", back_populates="record")


class DiagnosisResult(Base):
    """诊断结果详情表"""
    __tablename__ = "diagnosis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("diagnosis_records.id"))
    
    model_name = Column(String(50))
    model_type = Column(String(20))
    
    disease_name = Column(String(100))
    disease_name_en = Column(String(100))
    confidence = Column(Float)
    
    lesion_box = Column(JSON)
    lesion_type = Column(String(50))
    
    processing_time = Column(Float)
    
    created_at = Column(DateTime, default=datetime.now)
    
    record = relationship("DiagnosisRecord", back_populates="results")
