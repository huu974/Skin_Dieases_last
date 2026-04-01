"""
智肤康·皮肤疾病AI全流程辅助诊疗系统
FastAPI后端服务主入口
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from app.core.config import settings
from app.core.database import Base, engine
from app.api import auth, diagnosis, chat, knowledge, system

# 创建数据库表
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    print(f"🚀 {settings.APP_NAME} 启动中...")
    print(f"📋 版本: {settings.APP_VERSION}")
    print(f"🗄️  数据库: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")
    print(f"📡 Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    
    # 加载AI模型
    from app.services.ai_model import ai_model_service
    await ai_model_service.load_models()
    
    yield
    
    print(f"🛑 {settings.APP_NAME} 关闭中...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## 功能概述
    
    智肤康皮肤疾病AI辅助诊疗系统后端服务，提供以下核心功能：
    
    ### 1. 用户管理
    - 用户注册、登录、JWT认证
    - 个人信息CRUD
    - 权限管理
    - 访客模式支持
    
    ### 2. AI诊断
    - 皮肤病图像分类（多模型支持）
    - 病灶检测（YOLO）
    - 单模型/多模型/集成诊断
    - 返回置信度、病名、病灶坐标
    
    ### 3. 诊断业务
    - 诊断记录存储
    - PDF报告生成
    - 历史记录查询
    - 相似病例匹配（向量数据库）
    
    ### 4. 智能对话
    - 多模态对话（文本+图片）
    - RAG知识检索
    - 医疗术语标注
    - 风险评估
    - 转诊指引（地图API）
    
    ### 5. 预防建议
    - 疾病知识库
    - 个性化建议生成
    - 季节性疾病推送
    
    ### 6. 隐私安全
    - 医疗数据对称加密
    - 数据授权开关
    - 数据脱敏
    - 符合医疗数据安全法规
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加请求处理时间"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 3))
    return response


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """简单限流中间件"""
    try:
        from app.core.redis import redis_client
        
        client_ip = request.client.host
        rate_key = f"rate:{client_ip}"
        
        request_count = redis_client.get(rate_key)
        
        if request_count and int(request_count) > 100:
            return JSONResponse(
                status_code=429,
                content={"detail": "请求过于频繁，请稍后再试"}
            )
        
        redis_client.incr(rate_key)
        redis_client.expire(rate_key, 60)
    except Exception:
        pass  # Redis连接失败时跳过限流
    
    response = await call_next(request)
    return response


# 注册路由
app.include_router(auth.router)
app.include_router(diagnosis.router)
app.include_router(chat.router)
app.include_router(knowledge.router)
app.include_router(system.router)


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
