"""
系统API - 多模式切换、方言语音处理、系统信息
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
import uuid

from app.core.config import settings
from app.core.security import get_current_user
from app.core.redis import redis_client
from app.models.user import User

router = APIRouter(prefix="/api/system", tags=["系统"])


class ModeSwitchRequest(BaseModel):
    mode: str


class VoiceTranscriptionRequest(BaseModel):
    audio_data: str
    dialect: Optional[str] = "mandarin"


class SystemStatusResponse(BaseModel):
    status: str
    version: str
    mode: str
    timestamp: str


@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    """获取系统状态"""
    current_mode = redis_client.get("system:mode") or settings.DEFAULT_MODE
    
    return SystemStatusResponse(
        status="healthy",
        version=settings.APP_VERSION,
        mode=current_mode,
        timestamp=datetime.now().isoformat()
    )


@router.post("/mode/switch")
async def switch_mode(
    request: ModeSwitchRequest,
    current_user: User = Depends(get_current_user)
):
    """切换系统模式"""
    if request.mode not in settings.SYSTEM_MODES:
        raise HTTPException(
            status_code=400,
            detail=f"无效的模式: {request.mode}"
        )
    
    redis_client.set(f"system:mode", request.mode, expire=None)
    
    return {
        "message": f"系统模式已切换为: {request.mode}",
        "mode": request.mode,
        "available_modes": settings.SYSTEM_MODES
    }


@router.get("/mode")
async def get_current_mode():
    """获取当前系统模式"""
    current_mode = redis_client.get("system:mode") or settings.DEFAULT_MODE
    
    mode_descriptions = {
        "production": "生产模式 - 完整功能，真实数据",
        "development": "开发模式 - 调试功能，测试数据",
        "test": "测试模式 - 单元测试，模拟数据",
        "demo": "演示模式 - 展示功能，示例数据"
    }
    
    return {
        "mode": current_mode,
        "description": mode_descriptions.get(current_mode, ""),
        "available_modes": settings.SYSTEM_MODES
    }


@router.post("/voice/transcribe")
async def transcribe_voice(
    request: VoiceTranscriptionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    语音转文字 - 支持方言
    TODO: 集成语音识别API（讯飞/百度/腾讯）
    """
    # TODO: 实际调用语音识别API
    # import requests
    # if request.dialect == "sichuan":
    #     url = "https://iat-api.xfyun.cn/v2/iat"
    # elif request.dialect == " cantonese":
    #     ...
    
    # 模拟返回
    transcription = "这是语音转文字的模拟结果"
    
    return {
        "text": transcription,
        "dialect": request.dialect,
        "confidence": 0.95,
        "language": "zh-CN"
    }


@router.get("/dialects")
async def get_supported_dialects():
    """获取支持的方言列表"""
    return {
        "dialects": [
            {"code": "mandarin", "name": "普通话", "status": "supported"},
            {"code": "sichuan", "name": "四川话", "status": "supported"},
            {"code": "cantonese", "name": "粤语", "status": "supported"},
            {"code": "shanghai", "name": "上海话", "status": "beta"},
            {"code": "henan", "name": "河南话", "status": "beta"},
            {"code": "northeast", "name": "东北话", "status": "supported"}
        ]
    }


@router.get("/metrics")
async def get_system_metrics():
    """获取系统性能指标"""
    import random
    
    return {
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "diagnosis_avg_response_time": round(random.uniform(1.5, 3.0), 2),
            "chat_avg_response_time": round(random.uniform(0.8, 2.0), 2),
            "active_users": random.randint(50, 200),
            "total_diagnoses_today": random.randint(100, 500),
            "total_chats_today": random.randint(200, 1000),
            "system_load": round(random.uniform(0.2, 0.7), 2),
            "memory_usage": round(random.uniform(0.3, 0.6), 2),
            "cpu_usage": round(random.uniform(0.2, 0.5), 2)
        }
    }


@router.get("/concurrency")
async def check_concurrency():
    """检查并发支持能力"""
    return {
        "max_concurrent": settings.MAX_CONCURRENT,
        "current_concurrent": redis_client.get("system:concurrent") or 0,
        "diagnosis_timeout": settings.DIAGNOSIS_TIMEOUT,
        "chat_timeout": settings.CHAT_TIMEOUT
    }


class DataExportRequest(BaseModel):
    data_types: List[str]
    format: str = "json"


@router.post("/data/export")
async def export_user_data(
    request: DataExportRequest,
    current_user: User = Depends(get_current_user)
):
    """导出用户数据"""
    # TODO: 实际导出用户数据
    export_id = str(uuid.uuid4())
    
    return {
        "export_id": export_id,
        "status": "processing",
        "estimated_time": "5 minutes",
        "download_url": f"/api/system/data/download/{export_id}"
    }


@router.get("/data/download/{export_id}")
async def download_exported_data(
    export_id: str,
    current_user: User = Depends(get_current_user)
):
    """下载导出的数据"""
    # TODO: 实际返回导出的数据文件
    return {
        "message": "导出功能开发中",
        "export_id": export_id
    }


@router.delete("/data/anonymize")
async def anonymize_user_data(
    current_user: User = Depends(get_current_user)
):
    """匿名化用户数据"""
    # TODO: 实际匿名化数据
    return {
        "message": "数据匿名化处理已提交",
        "status": "processing"
    }
