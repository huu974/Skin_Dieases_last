"""
智能对话API - 多模态对话、医疗术语标注、风险评估、转诊指引
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, get_optional_user
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.schemas.chat import (
    ChatMessageCreate, ChatResponse, ChatSessionCreate,
    ChatSessionResponse, ChatHistoryResponse, ChatMessageResponse,
    QuickQuestionsResponse
)
from app.services.llm_chat import llm_chat_service
from app.services.map_service import map_service

router = APIRouter(prefix="/api/chat", tags=["智能对话"])


@router.post("", response_model=ChatResponse)
async def send_message(
    message: str = Form(...),
    session_id: Optional[str] = Form(None),
    diagnosis_context: Optional[str] = Form(None),
    images: Optional[List[str]] = Form(None),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    发送对话消息
    - 支持文本+图片多模态
    - RAG检索知识
    - 风险评估
    - 转诊建议
    """
    context = None
    if diagnosis_context:
        import json
        try:
            context = json.loads(diagnosis_context)
        except:
            pass
    
    result = await llm_chat_service.chat(
        message=message,
        context=context,
        images=images
    )
    
    if not session_id:
        session_id = str(uuid.uuid4())
    
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id
    ).first()
    
    if not session:
        session = ChatSession(
            session_id=session_id,
            user_id=current_user.id if current_user else None,
            title=message[:50]
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    
    user_message = ChatMessage(
        session_id=session.id,
        role="user",
        content=message,
        images=images
    )
    db.add(user_message)
    
    assistant_message = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=result["reply"],
        annotations=result.get("annotations"),
        reasoning_steps=result.get("reasoning_steps"),
        risk_assessment=result.get("risk_assessment"),
        referral_suggestion=result.get("referral_suggestion"),
        model_used="skin_diagnosis_agent",
        processing_time=result.get("processing_time", 0)
    )
    db.add(assistant_message)
    
    session.total_messages += 2
    session.updated_at = datetime.now()
    db.commit()
    
    if result.get("referral_suggestion", {}).get("suggested"):
        referral = result["referral_suggestion"]
        if referral.get("nearby_clinics") is None:
            clinics = await map_service.search_nearby_clinics(
                latitude=39.9,
                longitude=116.4,
                keyword="皮肤科"
            )
            referral["nearby_clinics"] = clinics[:3]
    
    return ChatResponse(
        reply=result["reply"],
        session_id=session_id,
        annotations=result.get("annotations"),
        reasoning_steps=result.get("reasoning_steps"),
        risk_assessment=result.get("risk_assessment"),
        referral_suggestion=result.get("referral_suggestion"),
        processing_time=result.get("processing_time", 0),
        timestamp=datetime.now()
    )


@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取对话会话列表"""
    query = db.query(ChatSession)
    
    if current_user:
        query = query.filter(ChatSession.user_id == current_user.id)
    else:
        query = query.filter(ChatSession.user_id.is_(None))
    
    sessions = query.order_by(ChatSession.updated_at.desc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()
    
    return [ChatSessionResponse.model_validate(s) for s in sessions]


@router.get("/sessions/{session_id}/history", response_model=ChatHistoryResponse)
async def get_history(
    session_id: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取会话历史"""
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    if current_user and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此会话")
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.created_at.asc()).all()
    
    return ChatHistoryResponse(
        session_id=session_id,
        messages=[ChatMessageResponse.model_validate(m) for m in messages],
        total=len(messages)
    )


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """删除会话"""
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    if current_user and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此会话")
    
    db.query(ChatMessage).filter(ChatMessage.session_id == session.id).delete()
    db.delete(session)
    db.commit()
    
    return {"message": "会话已删除"}


@router.get("/quick-questions", response_model=QuickQuestionsResponse)
async def get_quick_questions():
    """获取快捷问题"""
    questions = await llm_chat_service.get_quick_questions()
    return QuickQuestionsResponse(questions=questions)


@router.post("/clinics/nearby")
async def search_nearby_clinics(
    latitude: float = Form(...),
    longitude: float = Form(...),
    radius: float = Form(5000),
    keyword: str = Form("皮肤科")
):
    """搜索附近皮肤科诊所"""
    clinics = await map_service.search_nearby_clinics(
        latitude, longitude, radius, keyword
    )
    return {"clinics": clinics}


@router.post("/export")
async def export_conversation(
    session_id: str = Form(...),
    format: str = Form("json"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """导出对话记录"""
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    if current_user and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权导出此会话")
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.created_at.asc()).all()
    
    export_data = {
        "session_id": session_id,
        "title": session.title,
        "exported_at": datetime.now().isoformat(),
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "timestamp": m.created_at.isoformat()
            }
            for m in messages
        ]
    }
    
    return export_data
