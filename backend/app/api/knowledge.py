"""
预防建议API - 知识库、个性化建议、季节性疾病推送
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import calendar

from app.core.database import get_db
from app.models.knowledge import DiseaseKnowledge, PreventionAdvice, SeasonalPush
from app.schemas.knowledge import (
    DiseaseKnowledgeResponse, DiseaseKnowledgeListResponse,
    PreventionAdviceResponse, PersonalizedAdviceRequest,
    PersonalizedAdviceResponse, SeasonalDiseaseResponse,
    KnowledgeSearchRequest, KnowledgeSearchResponse
)

router = APIRouter(prefix="/api/knowledge", tags=["知识库"])


@router.get("/diseases", response_model=DiseaseKnowledgeListResponse)
async def get_diseases(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取疾病知识列表"""
    query = db.query(DiseaseKnowledge).filter(DiseaseKnowledge.is_published == True)
    
    if category:
        query = query.filter(DiseaseKnowledge.category == category)
    if severity:
        query = query.filter(DiseaseKnowledge.severity == severity)
    
    total = query.count()
    diseases = query.order_by(DiseaseKnowledge.view_count.desc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()
    
    return DiseaseKnowledgeListResponse(
        page=page,
        page_size=page_size,
        total=total,
        diseases=[DiseaseKnowledgeResponse.model_validate(d) for d in diseases]
    )


@router.get("/diseases/{disease_id}", response_model=DiseaseKnowledgeResponse)
async def get_disease_detail(disease_id: int, db: Session = Depends(get_db)):
    """获取疾病详情"""
    disease = db.query(DiseaseKnowledge).filter(
        DiseaseKnowledge.id == disease_id
    ).first()
    
    if not disease:
        raise HTTPException(status_code=404, detail="疾病不存在")
    
    disease.view_count += 1
    db.commit()
    
    return DiseaseKnowledgeResponse.model_validate(disease)


@router.get("/diseases/name/{disease_name}", response_model=DiseaseKnowledgeResponse)
async def get_disease_by_name(disease_name: str, db: Session = Depends(get_db)):
    """根据名称获取疾病"""
    disease = db.query(DiseaseKnowledge).filter(
        DiseaseKnowledge.disease_name == disease_name
    ).first()
    
    if not disease:
        raise HTTPException(status_code=404, detail="疾病不存在")
    
    return DiseaseKnowledgeResponse.model_validate(disease)


@router.get("/advice/{disease_name}", response_model=PreventionAdviceResponse)
async def get_prevention_advice(
    disease_name: str,
    db: Session = Depends(get_db)
):
    """获取疾病预防建议"""
    advice = db.query(PreventionAdvice).filter(
        PreventionAdvice.disease_name == disease_name,
        PreventionAdvice.is_active == True
    ).first()
    
    if not advice:
        return PreventionAdviceResponse(
            id=0,
            disease_id=0,
            disease_name=disease_name,
            prevention_tips=["保持皮肤清洁", "避免刺激", "及时就医"],
            dietary_advice=["均衡饮食", "多喝水", "避免辛辣"],
            nursing_advice=["保持湿润", "避免抓挠", "遵医嘱用药"]
        )
    
    return PreventionAdviceResponse.model_validate(advice)


@router.post("/advice/personalized", response_model=PersonalizedAdviceResponse)
async def get_personalized_advice(
    request: PersonalizedAdviceRequest,
    db: Session = Depends(get_db)
):
    """获取个性化建议"""
    disease_name = request.disease_name or "通用"
    
    advice = db.query(PreventionAdvice).filter(
        PreventionAdvice.disease_name == disease_name,
        PreventionAdvice.is_active == True
    ).first()
    
    general_advice = [
        "保持皮肤清洁干燥",
        "穿透气性好的衣物",
        "避免过度抓挠",
        "规律作息"
    ]
    
    personalized_advice = []
    if request.skin_type == "干性":
        personalized_advice.append("使用保湿霜，保持皮肤水分")
    elif request.skin_type == "油性":
        personalized_advice.append("使用控油护肤品，注意清洁")
    
    if request.allergies:
        personalized_advice.append(f"避免接触已知过敏原")
    
    seasonal_advice = _get_seasonal_advice(request.season)
    
    dietary_recommendations = [
        "均衡饮食，摄入足够维生素",
        "多喝水，保持身体水分",
        "避免辛辣刺激性食物"
    ]
    
    return PersonalizedAdviceResponse(
        disease_name=disease_name,
        general_advice=general_advice,
        personalized_advice=personalized_advice,
        seasonal_advice=seasonal_advice,
        dietary_recommendations=dietary_recommendations
    )


@router.get("/seasonal", response_model=SeasonalDiseaseResponse)
async def get_seasonal_diseases(
    season: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取季节性疾病信息"""
    if not season:
        month = datetime.now().month
        if month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        elif month in [9, 10, 11]:
            season = "autumn"
        else:
            season = "winter"
    
    seasonal_data = {
        "spring": {
            "diseases": [
                {"name": "过敏性皮炎", "prevalence": "高"},
                {"name": "荨麻疹", "prevalence": "高"},
                {"name": "湿疹", "prevalence": "中"}
            ],
            "tips": ["注意花粉过敏", "外出戴口罩", "及时更换衣物"]
        },
        "summer": {
            "diseases": [
                {"name": "痤疮", "prevalence": "高"},
                {"name": "毛囊炎", "prevalence": "高"},
                {"name": "日晒性皮炎", "prevalence": "中"}
            ],
            "tips": ["注意防晒", "保持皮肤清洁", "避免长时间日晒"]
        },
        "autumn": {
            "diseases": [
                {"name": "银屑病", "prevalence": "高"},
                {"name": "干燥性皮炎", "prevalence": "中"}
            ],
            "tips": ["保持皮肤湿润", "适当补水", "注意保暖"]
        },
        "winter": {
            "diseases": [
                {"name": "湿疹", "prevalence": "高"},
                {"name": "皮肤瘙痒症", "prevalence": "高"},
                {"name": "冻疮", "prevalence": "中"}
            ],
            "tips": ["注意保暖", "使用保湿产品", "避免热水烫洗"]
        }
    }
    
    data = seasonal_data.get(season, seasonal_data["spring"])
    
    return SeasonalDiseaseResponse(
        season=season,
        diseases=data["diseases"],
        prevention_tips=data["tips"]
    )


@router.post("/search", response_model=KnowledgeSearchResponse)
async def search_knowledge(
    request: KnowledgeSearchRequest,
    db: Session = Depends(get_db)
):
    """搜索知识库"""
    query = db.query(DiseaseKnowledge).filter(
        DiseaseKnowledge.is_published == True
    )
    
    if request.query:
        search_term = f"%{request.query}%"
        query = query.filter(
            (DiseaseKnowledge.disease_name.like(search_term)) |
            (DiseaseKnowledge.description.like(search_term)) |
            (DiseaseKnowledge.symptoms.like(search_term))
        )
    
    if request.category:
        query = query.filter(DiseaseKnowledge.category == request.category)
    if request.severity:
        query = query.filter(DiseaseKnowledge.severity == request.severity)
    
    results = query.limit(20).all()
    
    return KnowledgeSearchResponse(
        results=[DiseaseKnowledgeResponse.model_validate(r) for r in results],
        total=len(results)
    )


def _get_seasonal_advice(season: Optional[str]) -> List[str]:
    """获取季节性建议"""
    if not season:
        month = datetime.now().month
        if month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        elif month in [9, 10, 11]:
            season = "autumn"
        else:
            season = "winter"
    
    advice_map = {
        "spring": ["注意花粉过敏", "外出佩戴口罩", "勤换衣物"],
        "summer": ["注意防晒", "保持皮肤清洁", "穿透气衣物"],
        "autumn": ["保持皮肤湿润", "适当补水", "注意保暖"],
        "winter": ["注意保暖", "使用保湿产品", "避免过度洗澡"]
    }
    
    return advice_map.get(season, advice_map["spring"])
