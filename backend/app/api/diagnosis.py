"""
诊断API - AI诊断、记录管理、PDF报告、相似病例
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import tempfile
import time
import uuid
import hashlib
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user
from app.models.user import User
from app.models.diagnosis import DiagnosisRecord, DiagnosisResult
from app.schemas.diagnosis import (
    DiagnosisRequest, DiagnosisResponse, DiagnosisRecordResponse,
    DiagnosisListResponse, SimilarCasesResponse, PDFReportResponse
)
from app.services.ai_model import ai_model_service
from app.services.vector_db import vector_db_service
from app.services.pdf_report import pdf_report_service

router = APIRouter(prefix="/api/diagnosis", tags=["诊断"])


@router.post("/predict", response_model=DiagnosisResponse)
async def diagnose(
    image: UploadFile = File(...),
    models: Optional[str] = Form(None),
    diagnosis_mode: str = Form("single"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    AI皮肤诊断
    - 支持单模型和多模型诊断
    - 返回诊断结果、置信度、病灶坐标
    """
    start_time = time.time()
    
    image_data = await image.read()
    image_hash = hashlib.md5(image_data).hexdigest()
    
    session_id = str(uuid.uuid4())
    
    model_config = {
        "use_yolo": True,
        "use_classification": True,
        "classification_model": "efficientnet_b3"
    }
    
    if models:
        model_list = models.split(",")
    else:
        model_list = ["efficientnet_b3"]
    
    detection_result = None
    if model_config["use_yolo"]:
        detection_result = await ai_model_service.detect_lesions(image_data)
    
    if diagnosis_mode == "ensemble" and len(model_list) > 1:
        ensemble_result = await ai_model_service.ensemble_diagnosis(
            image_data, model_list
        )
        classification_result = {
            "model_used": "ensemble",
            "top1": {
                "class": ensemble_result["primary_disease"],
                "probability": ensemble_result["primary_confidence"]
            },
            "top5": []
        }
        all_results = ensemble_result["all_results"]
    else:
        classification_result, _ = await ai_model_service.classify_disease(
            image_data, model_list[0]
        )
        all_results = [{
            "model_name": model_list[0],
            "model_type": "classification",
            "disease_name": classification_result["top1"]["class"],
            "disease_name_en": classification_result["top1"]["class_en"],
            "confidence": classification_result["top1"]["probability"],
            "lesion_box": detection_result["boxes"][0] if detection_result else None,
            "processing_time": 0
        }]
    
    risk_level = "low"
    if classification_result["top1"]["probability"] < 0.6:
        risk_level = "medium"
    if classification_result["top1"]["probability"] < 0.4:
        risk_level = "high"
    
    recommendation = _generate_recommendation(
        classification_result["top1"]["class"],
        risk_level
    )
    
    record = DiagnosisRecord(
        user_id=current_user.id if current_user else None,
        session_id=session_id,
        image_path="",
        image_hash=image_hash,
        models_used=model_list,
        diagnosis_mode=diagnosis_mode,
        detection_result=detection_result,
        classification_result=classification_result,
        primary_disease=classification_result["top1"]["class"],
        primary_confidence=classification_result["top1"]["probability"],
        all_results=all_results,
        lesion_coordinates=detection_result["boxes"] if detection_result else [],
        risk_level=risk_level,
        recommendation=recommendation
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    for result in all_results:
        db_result = DiagnosisResult(
            record_id=record.id,
            model_name=result["model_name"],
            model_type=result["model_type"],
            disease_name=result["disease_name"],
            disease_name_en=result.get("disease_name_en", ""),
            confidence=result["confidence"],
            lesion_box=result.get("lesion_box"),
            processing_time=result.get("processing_time", 0)
        )
        db.add(db_result)
    db.commit()
    
    processing_time = time.time() - start_time
    
    return DiagnosisResponse(
        record_id=record.id,
        session_id=session_id,
        detection=detection_result,
        classification=classification_result,
        primary_disease=classification_result["top1"]["class"],
        primary_confidence=classification_result["top1"]["probability"],
        all_results=all_results,
        lesion_coordinates=detection_result["boxes"] if detection_result else [],
        risk_level=risk_level,
        recommendation=recommendation,
        processing_time=round(processing_time, 2),
        models_used=model_list,
        timestamp=record.created_at
    )


@router.get("/models")
async def get_available_models():
    """获取可用AI模型"""
    return {
        "models": ai_model_service.get_available_models()
    }


@router.get("/history", response_model=DiagnosisListResponse)
async def get_diagnosis_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取诊断历史"""
    query = db.query(DiagnosisRecord)
    
    if current_user:
        query = query.filter(DiagnosisRecord.user_id == current_user.id)
    else:
        query = query.filter(DiagnosisRecord.user_id.is_(None))
    
    total = query.count()
    records = query.order_by(DiagnosisRecord.created_at.desc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()
    
    return DiagnosisListResponse(
        page=page,
        page_size=page_size,
        total=total,
        records=[
            DiagnosisRecordResponse(
                id=r.id,
                user_id=r.user_id,
                session_id=r.session_id,
                image_path=r.image_path,
                primary_disease=r.primary_disease,
                primary_confidence=r.primary_confidence,
                risk_level=r.risk_level,
                created_at=r.created_at
            )
            for r in records
        ]
    )


@router.get("/{record_id}", response_model=DiagnosisResponse)
async def get_diagnosis_detail(
    record_id: int,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取诊断详情"""
    record = db.query(DiagnosisRecord).filter(DiagnosisRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="诊断记录不存在")
    
    if current_user and record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此记录")
    
    return DiagnosisResponse(
        record_id=record.id,
        session_id=record.session_id,
        detection=record.detection_result,
        classification=record.classification_result,
        primary_disease=record.primary_disease,
        primary_confidence=record.primary_confidence,
        all_results=record.all_results,
        lesion_coordinates=record.lesion_coordinates,
        risk_level=record.risk_level,
        recommendation=record.recommendation,
        processing_time=0,
        models_used=record.models_used,
        timestamp=record.created_at
    )


@router.delete("/{record_id}")
async def delete_diagnosis(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除诊断记录"""
    record = db.query(DiagnosisRecord).filter(
        DiagnosisRecord.id == record_id,
        DiagnosisRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    db.query(DiagnosisResult).filter(DiagnosisResult.record_id == record_id).delete()
    db.delete(record)
    db.commit()
    
    return {"message": "记录已删除"}


@router.get("/{record_id}/similar", response_model=SimilarCasesResponse)
async def get_similar_cases(
    record_id: int,
    top_k: int = Query(5, ge=1, le=20),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取相似病例"""
    record = db.query(DiagnosisRecord).filter(DiagnosisRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    embedding = await vector_db_service.get_embedding(record.image_path)
    similar_cases = await vector_db_service.search_similar(embedding, top_k)
    
    return SimilarCasesResponse(
        record_id=record_id,
        similar_cases=similar_cases
    )


@router.post("/{record_id}/report", response_model=PDFReportResponse)
async def generate_report(
    record_id: int,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """生成诊断报告PDF"""
    record = db.query(DiagnosisRecord).filter(DiagnosisRecord.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    diagnosis_data = {
        "primary_disease": record.primary_disease,
        "primary_confidence": record.primary_confidence,
        "all_results": record.all_results,
        "recommendation": record.recommendation,
        "timestamp": record.created_at.isoformat()
    }
    
    user_data = None
    if current_user:
        user_data = {
            "name": current_user.username,
            "email": current_user.email
        }
    
    report = await pdf_report_service.generate_report(
        record_id, diagnosis_data, user_data
    )
    
    record.pdf_report_path = report["report_path"]
    db.commit()
    
    return PDFReportResponse(**report)


@router.get("/report/{report_id}/download")
async def download_report(report_id: str):
    """下载诊断报告"""
    report = await pdf_report_service.get_report(report_id)
    
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    return FileResponse(
        report["report_path"],
        media_type="application/pdf",
        filename=f"diagnosis_report_{report_id}.pdf"
    )


def _generate_recommendation(disease: str, risk_level: str) -> str:
    """生成建议"""
    recommendations = {
        "银屑病": "建议：保持皮肤湿润，避免过度洗澡，减少精神压力。如症状加重请就医。",
        "湿疹": "建议：避免接触过敏原，保持皮肤清洁湿润，使用温和的护肤品。",
        "痤疮": "建议：保持面部清洁，不要挤压痘痘，规律作息，减少高糖饮食。",
        "荨麻疹": "建议：查找并避免过敏原，冷敷缓解瘙痒，避免抓挠。",
    }
    
    base = recommendations.get(disease, "建议：注意皮肤护理，如症状持续请就医。")
    
    if risk_level == "high":
        base += "\n⚠️ 风险等级较高，建议尽快就医。"
    elif risk_level == "medium":
        base += "\n建议密切关注症状变化，如有加重请及时就医。"
    
    return base
