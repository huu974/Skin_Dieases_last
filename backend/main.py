"""
FastAPI 后端入口
皮肤病智能诊断系统 API
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import sys
import tempfile
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="皮肤病智能诊断系统 API", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 数据模型 ============

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    diagnosis_context: Optional[dict] = None

class UserProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    skin_type: Optional[str] = None
    allergies: Optional[str] = None

# ============ 模拟数据存储（生产环境用数据库）============

# 用户存储 {username: {password, email, ...}}
users_db = {}

# 历史记录存储
diagnosis_history = []

# 当前登录用户
current_user = {"username": "", "token": ""}

# 用户信息存储
user_profiles = {
    "default": {
        "name": "访客用户",
        "email": "",
        "phone": "",
        "age": 25,
        "gender": "未设置",
        "skin_type": "普通",
        "allergies": "",
        "theme": "light",
        "language": "中文"
    }
}

# 对话历史
chat_sessions = {}


# ============ API 路由 ============

@app.get("/")
async def root():
    return {"message": "皮肤病智能诊断系统 API", "version": "1.0.0"}


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ============ 检测与分类 API ============

@app.post("/api/detect")
async def detect_and_classify(
    image: UploadFile = File(...),
    model: Optional[str] = Form("efficientnet_b3")
):
    """
    图像检测与分类 API
    - 使用 YOLO 检测皮损区域
    - 使用 CNN 分类皮肤病类型
    """
    try:
        # 保存上传的图像
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image.filename.split('.')[-1]}") as tmp:
            content = await image.read()
            tmp.write(content)
            tmp_path = tmp.name

        # TODO: 调用实际的模型进行预测
        # 这里返回模拟数据，实际需要调用:
        # from model.yolo_detector import YOLOv10Detector
        # from model.PanDerm import MyModel
        
        # 模拟检测结果
        result = {
            "detection_boxes": [[120, 80, 320, 280]],
            "detection_classes": ["病变区域"],
            "detection_confidences": [0.95],
            "cropped_regions": [tmp_path],  # 裁剪后的图像路径
            "classification": {
                "model_used": model,
                "top1": {
                    "class": "银屑病",
                    "class_en": "Psoriasis",
                    "probability": 0.87
                },
                "top5": [
                    {"class": "银屑病", "class_en": "Psoriasis", "probability": 0.87},
                    {"class": "湿疹", "class_en": "Eczema", "probability": 0.06},
                    {"class": "特应性皮炎", "class_en": "Atopic Dermatitis", "probability": 0.04},
                    {"class": "脂溢性皮炎", "class_en": "Seborrheic Dermatitis", "probability": 0.02},
                    {"class": "扁平苔藓", "class_en": "Lichen Planus", "probability": 0.01}
                ]
            },
            "timestamp": datetime.now().isoformat()
        }

        # 保存到历史记录
        record = {
            "id": len(diagnosis_history) + 1,
            "image_path": tmp_path,
            "image_name": image.filename,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        diagnosis_history.append(record)

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")


# ============ 智能对话 API ============

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    智能对话 API
    - 基于 RAG + Agent 的智能问诊
    """
    try:
        session_id = request.session_id or "default"
        
        # 初始化会话
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # 添加用户消息
        chat_sessions[session_id].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        })

        # TODO: 调用实际的 RAG + Agent
        # from agent.react_agent import SkinDiagnosisAgent
        # agent = SkinDiagnosisAgent()
        # response, steps = agent.chat_with_reasoning(request.message)

        # 模拟回复
        response_text = f"根据您描述的症状：{request.message}\n\n这可能是常见的皮肤炎症反应。建议：\n\n1. 保持患处清洁干燥\n2. 避免使用刺激性护肤品\n3. 如症状持续或加重，请尽快就医\n\n⚠️ 本回答仅供参考，不作为正式医疗诊断。"
        
        reasoning_steps = [
            {"step": "思考", "content": "用户描述了皮肤症状，需要分析可能的皮肤病类型"},
            {"step": "检索", "content": "查询RAG知识库中相关的皮肤病症状描述"},
            {"step": "分析", "content": "根据症状匹配，最可能是皮肤炎症或湿疹"},
            {"step": "建议", "content": "给出一般性护理建议和就医提醒"}
        ]

        # 添加AI回复
        chat_sessions[session_id].append({
            "role": "assistant",
            "content": response_text,
            "steps": reasoning_steps,
            "timestamp": datetime.now().isoformat()
        })

        return {
            "reply": response_text,
            "steps": reasoning_steps,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")


@app.get("/api/chat/history")
async def get_chat_history(session_id: str = "default"):
    """获取对话历史"""
    return {
        "session_id": session_id,
        "history": chat_sessions.get(session_id, [])
    }


@app.delete("/api/chat/history")
async def clear_chat_history(session_id: str = "default"):
    """清空对话历史"""
    if session_id in chat_sessions:
        chat_sessions[session_id] = []
    return {"message": "对话历史已清空"}


# ============ 历史记录 API ============

@app.get("/api/history")
async def get_history(page: int = 1, size: int = 10):
    """获取诊断历史记录"""
    start = (page - 1) * size
    end = start + size
    
    records = diagnosis_history[start:end]
    total = len(diagnosis_history)
    
    return {
        "page": page,
        "size": size,
        "total": total,
        "records": [
            {
                "id": r["id"],
                "image_name": r["image_name"],
                "result": r["result"],
                "timestamp": r["timestamp"]
            }
            for r in records
        ]
    }


@app.get("/api/history/{record_id}")
async def get_history_detail(record_id: int):
    """获取单条诊断详情"""
    for record in diagnosis_history:
        if record["id"] == record_id:
            return record
    raise HTTPException(status_code=404, detail="记录不存在")


@app.delete("/api/history/{record_id}")
async def delete_history(record_id: int):
    """删除诊断记录"""
    global diagnosis_history
    diagnosis_history = [r for r in diagnosis_history if r["id"] != record_id]
    return {"message": "记录已删除"}


# ============ 用户中心 API ============

@app.get("/api/user/profile")
async def get_user_profile(user_id: str = "default"):
    """获取用户信息"""
    return user_profiles.get(user_id, user_profiles["default"])


@app.put("/api/user/profile")
async def update_user_profile(profile: UserProfile, user_id: str = "default"):
    """更新用户信息"""
    if user_id in user_profiles:
        user_profiles[user_id].update(profile.dict(exclude_unset=True))
    else:
        user_profiles[user_id] = profile.dict()
    
    return {"message": "用户信息已更新", "profile": user_profiles[user_id]}


@app.post("/api/auth/register")
async def register(username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    """用户注册"""
    if username in users_db:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    users_db[username] = {
        "password": password,
        "email": email,
        "created_at": datetime.now().isoformat()
    }
    
    # 创建用户 profile
    user_profiles[username] = {
        "name": username,
        "email": email,
        "phone": "",
        "age": 25,
        "gender": "未设置",
        "skin_type": "普通",
        "allergies": "",
        "theme": "light",
        "language": "中文"
    }
    
    return {"message": "注册成功", "username": username}


@app.post("/api/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """用户登录"""
    if username not in users_db:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    if users_db[username]["password"] != password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    token = f"token_{username}_{datetime.now().timestamp()}"
    current_user["username"] = username
    current_user["token"] = token
    
    return {
        "token": token,
        "username": username,
        "email": users_db[username]["email"]
    }


@app.post("/api/auth/logout")
async def logout():
    """用户登出"""
    current_user["username"] = ""
    current_user["token"] = ""
    return {"message": "已退出登录"}


@app.get("/api/auth/status")
async def get_auth_status():
    """获取登录状态"""
    return {
        "is_logged_in": bool(current_user["username"]),
        "username": current_user["username"]
    }





# ============ 预防建议 API ============

@app.get("/api/advice")
async def get_advice(disease: Optional[str] = None):
    """获取预防建议"""
    advice_data = {
        "银屑病": {
            "预防": ["避免感染", "减少精神压力", "戒烟戒酒", "避免外伤"],
            "饮食": ["多吃蔬果", "补充Omega-3", "少吃牛羊肉"],
            "护理": ["保持皮肤湿润", "避免过度洗澡", "使用温和护肤品"]
        },
        "湿疹": {
            "预防": ["保持皮肤湿润", "避免接触过敏原", "穿棉质衣物", "适度洗澡"],
            "饮食": ["避免海鲜", "少吃辛辣", "补充维生素C"],
            "护理": ["使用保湿霜", "避免抓挠", "温水洗澡"]
        },
        "痤疮": {
            "预防": ["清洁面部", "不挤压痘痘", "规律作息", "卸妆彻底"],
            "饮食": ["少吃甜食", "避免油炸", "多喝水"],
            "护理": ["每天清洁", "使用控油产品", "避免用手触摸"]
        },
        "荨麻疹": {
            "预防": ["查找过敏原", "避免冷热刺激", "穿着宽松", "保持清洁"],
            "饮食": ["记录食物日记", "避免已知过敏食物"],
            "护理": ["冷敷缓解", "避免抓挠", "穿着宽松衣物"]
        }
    }
    
    if disease:
        return advice_data.get(disease, {"message": "未找到该疾病的建议"})
    return advice_data


# ============ 启动配置 ============

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
