"""
诊断相关Schema
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DiagnosisModelConfig(BaseModel):
    """诊断模型配置"""
    use_yolo: bool = True
    use_classification: bool = True
    classification_model: str = "efficientnet_b3"
    models_to_ensemble: Optional[List[str]] = None


class DiagnosisRequest(BaseModel):
    """诊断请求"""
    models: Optional[DiagnosisModelConfig] = None
    diagnosis_mode: str = "single"
    user_notes: Optional[str] = None


class DetectionResult(BaseModel):
    """检测结果"""
    boxes: List[List[float]]
    classes: List[str]
    confidences: List[float]
    cropped_regions: Optional[List[str]] = None


class ClassificationResult(BaseModel):
    """分类结果"""
    model_used: str
    top1: dict
    top5: List[dict]
    all_predictions: Optional[List[dict]] = None


class ModelDiagnosisResult(BaseModel):
    """单个模型的诊断结果"""
    model_name: str
    model_type: str
    disease_name: str
    disease_name_en: str
    confidence: float
    lesion_box: Optional[List[float]] = None
    processing_time: float


class DiagnosisResponse(BaseModel):
    """诊断响应"""
    record_id: int
    session_id: str
    
    detection: Optional[DetectionResult] = None
    classification: ClassificationResult
    
    primary_disease: str
    primary_confidence: float
    all_results: List[ModelDiagnosisResult]
    
    lesion_coordinates: List[dict]
    
    risk_level: str
    recommendation: str
    
    processing_time: float
    models_used: List[str]
    
    timestamp: datetime


class DiagnosisRecordResponse(BaseModel):
    """诊断记录响应"""
    id: int
    user_id: Optional[int] = None
    session_id: str
    image_path: str
    primary_disease: str
    primary_confidence: float
    risk_level: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DiagnosisListResponse(BaseModel):
    """诊断记录列表响应"""
    page: int
    page_size: int
    total: int
    records: List[DiagnosisRecordResponse]


class SimilarCase(BaseModel):
    """相似病例"""
    record_id: int
    similarity: float
    disease_name: str
    disease_name_en: str
    confidence: float
    created_at: datetime


class SimilarCasesResponse(BaseModel):
    """相似病例响应"""
    record_id: int
    similar_cases: List[SimilarCase]


class PDFReportResponse(BaseModel):
    """PDF报告响应"""
    report_id: int
    report_path: str
    download_url: str
    expires_at: datetime
