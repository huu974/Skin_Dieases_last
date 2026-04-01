"""
知识库相关Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DiseaseKnowledgeResponse(BaseModel):
    """疾病知识响应"""
    id: int
    disease_name: str
    disease_name_en: Optional[str] = None
    disease_code: Optional[str] = None
    
    category: Optional[str] = None
    severity: Optional[str] = None
    contagion: Optional[str] = None
    
    description: Optional[str] = None
    symptoms: Optional[str] = None
    causes: Optional[str] = None
    
    season_prevalence: Optional[dict] = None
    age_group: Optional[dict] = None
    
    view_count: int
    
    class Config:
        from_attributes = True


class DiseaseKnowledgeListResponse(BaseModel):
    """疾病知识列表响应"""
    page: int
    page_size: int
    total: int
    diseases: List[DiseaseKnowledgeResponse]


class PreventionAdviceResponse(BaseModel):
    """预防建议响应"""
    id: int
    disease_id: int
    disease_name: str
    
    prevention_tips: List[str]
    dietary_advice: List[str]
    nursing_advice: List[str]
    
    seasonal_advice: Optional[dict] = None
    
    class Config:
        from_attributes = True


class PersonalizedAdviceRequest(BaseModel):
    """个性化建议请求"""
    disease_name: Optional[str] = None
    user_age: Optional[int] = None
    user_gender: Optional[str] = None
    skin_type: Optional[str] = None
    season: Optional[str] = None
    allergies: Optional[List[str]] = None


class PersonalizedAdviceResponse(BaseModel):
    """个性化建议响应"""
    disease_name: str
    general_advice: List[str]
    personalized_advice: List[str]
    seasonal_advice: List[str]
    dietary_recommendations: List[str]


class SeasonalDiseaseResponse(BaseModel):
    """季节性疾病响应"""
    season: str
    diseases: List[dict]
    prevention_tips: List[str]


class KnowledgeSearchRequest(BaseModel):
    """知识库搜索请求"""
    query: str
    category: Optional[str] = None
    severity: Optional[str] = None


class KnowledgeSearchResponse(BaseModel):
    """知识库搜索响应"""
    results: List[DiseaseKnowledgeResponse]
    total: int
