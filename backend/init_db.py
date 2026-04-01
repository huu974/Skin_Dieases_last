"""
数据库初始化脚本
"""
from sqlalchemy import create_engine
from app.core.config import settings
from app.core.database import Base
from app.models.user import User, UserProfile, UserPermission
from app.models.diagnosis import DiagnosisRecord, DiagnosisResult
from app.models.chat import ChatSession, ChatMessage
from app.models.knowledge import DiseaseKnowledge, PreventionAdvice
from app.core.security import get_password_hash
from datetime import datetime


def init_database():
    """初始化数据库"""
    print("📊 初始化数据库...")
    
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    print("✅ 数据库表创建完成")
    
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("📝 初始化基础数据...")
    
    # 创建管理员用户
    admin = User(
        username="admin",
        email="admin@skindiagnosis.com",
        password_hash=get_password_hash("admin123"),
        role="admin",
        is_active=True,
        is_verified=True
    )
    session.add(admin)
    
    # 创建示例用户
    user = User(
        username="demo",
        email="demo@skindiagnosis.com",
        password_hash=get_password_hash("demo123"),
        role="user",
        is_active=True,
        is_verified=True
    )
    session.add(user)
    session.commit()
    
    # 创建用户资料
    profile = UserProfile(
        user_id=user.id,
        name="演示用户",
        age=30,
        gender="男",
        skin_type="普通",
        allergies=""
    )
    session.add(profile)
    
    # 添加疾病知识
    diseases = [
        {
            "disease_name": "银屑病",
            "disease_name_en": "Psoriasis",
            "category": "炎症性皮肤病",
            "severity": "慢性",
            "contagion": "非传染性",
            "description": "银屑病是一种慢性炎症性皮肤病，表现为皮肤红斑、鳞屑，可累及关节。",
            "symptoms": "红斑、鳞屑、瘙痒、关节疼痛",
            "causes": "遗传、免疫、环境因素",
            "season_prevalence": {"spring": "low", "summer": "medium", "autumn": "high", "winter": "high"},
            "age_group": {"min": 0, "max": 100}
        },
        {
            "disease_name": "湿疹",
            "disease_name_en": "Eczema",
            "category": "过敏性皮肤病",
            "severity": "慢性",
            "contagion": "非传染性",
            "description": "湿疹是皮肤炎症反应，伴随瘙痒和红斑。",
            "symptoms": "红斑、瘙痒、水疱、渗出",
            "causes": "过敏、遗传、环境",
            "season_prevalence": {"spring": "high", "summer": "medium", "autumn": "medium", "winter": "high"},
            "age_group": {"min": 0, "max": 60}
        },
        {
            "disease_name": "痤疮",
            "disease_name_en": "Acne",
            "category": "毛囊皮脂腺疾病",
            "severity": "慢性",
            "contagion": "非传染性",
            "description": "痤疮是毛囊皮脂腺单位的慢性炎症性疾病。",
            "symptoms": "粉刺、丘疹、脓疱、囊肿",
            "causes": "激素、油脂、细菌、遗传",
            "season_prevalence": {"spring": "medium", "summer": "high", "autumn": "medium", "winter": "low"},
            "age_group": {"min": 10, "max": 40}
        },
    ]
    
    for disease_data in diseases:
        disease = DiseaseKnowledge(**disease_data)
        session.add(disease)
    
    # 添加预防建议
    advices = [
        {
            "disease_id": 1,
            "disease_name": "银屑病",
            "prevention_tips": [
                "保持皮肤湿润",
                "避免过度洗澡",
                "减少精神压力",
                "戒烟戒酒",
                "避免外伤"
            ],
            "dietary_advice": [
                "多吃蔬果",
                "补充Omega-3",
                "少吃牛羊肉",
                "避免辛辣"
            ],
            "nursing_advice": [
                "使用温和的沐浴露",
                "坚持使用保湿霜",
                "避免抓挠",
                "适度日晒"
            ],
            "seasonal_advice": {
                "winter": "注意保暖，避免皮肤干燥",
                "summer": "注意防晒，避免过度出汗"
            }
        },
        {
            "disease_id": 2,
            "disease_name": "湿疹",
            "prevention_tips": [
                "保持皮肤湿润",
                "避免接触过敏原",
                "穿棉质衣物",
                "适度洗澡"
            ],
            "dietary_advice": [
                "避免海鲜",
                "少吃辛辣",
                "补充维生素C"
            ],
            "nursing_advice": [
                "使用保湿霜",
                "避免抓挠",
                "温水洗澡"
            ],
            "seasonal_advice": {
                "winter": "加强保湿",
                "spring": "注意过敏原"
            }
        },
    ]
    
    for advice_data in advices:
        advice = PreventionAdvice(**advice_data)
        session.add(advice)
    
    session.commit()
    
    print("✅ 基础数据初始化完成")
    print("")
    print("📌 账户信息:")
    print("   管理员: admin / admin123")
    print("   演示用户: demo / demo123")
    print("")
    print("🚀 数据库初始化完成，可以启动服务")


if __name__ == "__main__":
    init_database()
