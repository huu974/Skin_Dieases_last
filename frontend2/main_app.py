"""
皮肤病智能诊断系统 - 主入口
基于 Streamlit
医疗科技蓝白风格
"""

import streamlit as st
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import time
import uuid

# 页面配置
st.set_page_config(
    page_title="皮肤病变AI辅助诊断系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 样式配置 - 医疗科技风格
st.markdown("""
<style>
    /* 医疗科技风格 - 蓝色系 */
    :root {
        --primary: #1E88E5;
        --primary-dark: #0b5cab;
        --secondary: #00ACC1;
        --success: #2E7D32;
        --warning: #F9A825;
        --error: #D32F2F;
        --bg-page: #F8FAFC;
        --bg-card: #FFFFFF;
        --text-primary: #1E293B;
        --text-secondary: #475569;
        --text-placeholder: #94A3B8;
        --border: #E2E8F0;
    }
    
    /* 主背景 */
    .stApp {
        background: #F8FAFC;
        min-height: 100vh;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%) !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* 标题 */
    h1 { font-size: 32px !important; font-weight: 600 !important; color: #1E293B !important; line-height: 1.3 !important; }
    h2 { font-size: 24px !important; font-weight: 600 !important; color: #1E293B !important; line-height: 1.3 !important; }
    h3 { font-size: 20px !important; font-weight: 600 !important; color: #1E293B !important; line-height: 1.3 !important; }
    h4 { font-size: 18px !important; font-weight: 600 !important; color: #1E293B !important; line-height: 1.3 !important; }
    
    /* 段落文字 */
    p, span, div {
        color: #475569 !important;
        line-height: 1.5 !important;
    }
    
    /* 按钮 - 主按钮 */
    .stButton > button {
        background: #1E88E5 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #0b5cab !important;
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* 按钮 - 次按钮 */
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #1E88E5 !important;
        border: 1px solid #CBD5E1 !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #F1F5F9 !important;
    }
    
    /* 输入框 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: white !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        color: #1E293B !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #94A3B8 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #1E88E5 !important;
        box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.2) !important;
    }
    
    /* 标签页 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px 8px 0 0;
        color: #475569;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #1E88E5;
        color: white !important;
        font-weight: 600;
        border-color: #1E88E5;
    }
    
    /* 指标卡片 */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: 600;
        color: #1E88E5 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-size: 12px;
    }
    
    /* 分割线 */
    hr {
        border-color: #E2E8F0 !important;
    }
    
    /* 进度条 */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1E88E5 0%, #00ACC1 100%);
        border-radius: 4px;
    }
    
    /* 单选按钮 */
    .stRadio > div {
        color: #475569;
    }
    
    /* 下拉选择框 */
    .stSelectbox > div > div > div {
        background: white !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        color: #1E293B !important;
    }
    
    /* 警告/信息框 */
    .stAlert {
        background: white !important;
        border: 1px solid #E2E8F0 !important;
        color: #475569 !important;
        border-radius: 16px !important;
    }
    
    /* 复选框 */
    .stCheckbox > label {
        color: #475569 !important;
    }
    
    /* 滚动条 */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 3px;
    }
    
    /* 卡片 */
    .card {
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        padding: 20px;
    }
    
    .card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }
    
    /* 上传区域 */
    [data-testid="stFileUploader"] {
        background: #F8FAFC;
        border: 2px dashed #CBD5E1;
        border-radius: 16px;
        padding: 40px 20px;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #1E88E5;
        background: #F1F5F9;
    }
    
    /* 对话气泡 - 用户 */
    .chat-user {
        background: #1E88E5;
        color: white !important;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 16px;
    }
    
    /* 对话气泡 - AI */
    .chat-ai {
        background: #F1F5F9;
        color: #1E293B !important;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 16px;
    }
    
    /* 表格样式 */
    .dataframe {
        border: none !important;
    }
    
    .dataframe thead {
        background: #F8FAFC !important;
    }
    
    .dataframe tbody tr:hover {
        background: #F8FAFC !important;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"
if "language" not in st.session_state:
    st.session_state["language"] = "中文"
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "user_info" not in st.session_state:
    st.session_state["user_info"] = {
        "name": "访客用户", "email": "", "theme": "light", "language": "中文"
    }
if "diagnosis_records" not in st.session_state:
    st.session_state["diagnosis_records"] = [
        {"id": 1, "image_name": "skin_001.jpg", "disease": "银屑病", "disease_en": "Psoriasis", "confidence": 0.87, "timestamp": "2026-03-28 10:30:00"},
        {"id": 2, "image_name": "skin_002.jpg", "disease": "湿疹", "disease_en": "Eczema", "confidence": 0.76, "timestamp": "2026-03-27 15:20:00"},
    ]
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "assistant", "content": "🏥 您好！我是皮肤病智能诊断助手。请描述您遇到的皮肤问题？"}
    ]
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "诊断分析"
if "current_diagnosis" not in st.session_state:
    st.session_state["current_diagnosis"] = None


def login_page():
    """登录/注册页面 - 医疗科技风格"""
    st.markdown("""
    <style>
    .login-wrapper {
        max-width: 420px;
        margin: 60px auto;
        padding: 40px;
    }
    
    .login-card {
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        padding: 40px 35px;
    }
    
    .login-title {
        text-align: center;
        margin-bottom: 32px;
    }
    
    .login-title h1 {
        font-size: 28px !important;
        color: #1E88E5 !important;
        margin: 0 !important;
    }
    
    .login-title p {
        color: #475569;
        font-size: 14px;
        margin-top: 8px;
    }
    
    .test-info {
        background: #F8FAFC;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        color: #475569;
        font-size: 13px;
        margin-top: 20px;
    }
    
    .test-info strong {
        color: #1E88E5;
    }
    </style>
    
    <div class="login-wrapper">
        <div class="login-card">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="login-title">
            <h1>🏥 MedSkin</h1>
            <p>皮肤病变AI辅助诊断系统</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["🔑 登录", "📝 注册"])
        
        with tab_login:
            login_username = st.text_input("用户名", key="login_user")
            login_password = st.text_input("密码", type="password", key="login_pass")
            
            if st.button("登 录", type="primary", use_container_width=True):
                if login_username and login_password:
                    st.session_state["is_logged_in"] = True
                    st.session_state["username"] = login_username
                    st.session_state["user_info"]["name"] = login_username
                    st.rerun()
                else:
                    st.error("请输入用户名和密码")
            
            st.markdown("""
            <div class="test-info">
                测试账号: <strong>test</strong> | 密码: <strong>123456</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with tab_register:
            reg_username = st.text_input("用户名", key="reg_user")
            reg_email = st.text_input("邮箱", key="reg_email")
            reg_password = st.text_input("密码", type="password", key="reg_pass")
            reg_password2 = st.text_input("确认密码", type="password", key="reg_pass2")
            
            if st.button("注 册", type="primary", use_container_width=True):
                if reg_username and reg_email and reg_password:
                    if reg_password != reg_password2:
                        st.error("两次输入的密码不一致")
                    else:
                        st.session_state["is_logged_in"] = True
                        st.session_state["username"] = reg_username
                        st.session_state["user_info"]["name"] = reg_username
                        st.session_state["user_info"]["email"] = reg_email
                        st.success("注册成功！")
                        st.rerun()
                else:
                    st.error("请填写完整信息")
    
    st.markdown("</div></div>", unsafe_allow_html=True)


# 检查登录状态
if not st.session_state["is_logged_in"]:
    login_page()
    st.stop()


# ============ 页面函数 ============

def page_diagnosis():
    """诊断分析页面"""
    st.title("📊 诊断分析")
    st.caption("上传皮肤病变图像，AI自动进行检测与分类")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📤 图像上传")
        model_option = st.selectbox("选择分类模型", ["EfficientNet-B3 (推荐)", "ResNet50"])
        model_name = "efficientnet_b3" if "EfficientNet" in model_option else "resnet50"
        
        uploaded_file = st.file_uploader("选择皮肤病变图像", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="原始图像", use_container_width=True)
            
            if st.button("🔍 开始诊断", type="primary", use_container_width=True):
                with st.spinner("正在分析图像..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.03)
                    
                    # 模拟结果
                    boxes = [[50, 30, 250, 230]]
                    labels = ["病变区域"]
                    confidences = [0.95]
                    
                    top5_results = [
                        {"class": "银屑病", "class_en": "Psoriasis", "probability": 0.87},
                        {"class": "湿疹", "class_en": "Eczema", "probability": 0.06},
                        {"class": "特应性皮炎", "class_en": "Atopic Dermatitis", "probability": 0.04},
                        {"class": "脂溢性皮炎", "class_en": "Seborrheic Dermatitis", "probability": 0.02},
                        {"class": "扁平苔藓", "class_en": "Lichen Planus", "probability": 0.01}
                    ]
                    
                    st.session_state["current_diagnosis"] = {
                        "model_used": model_name, "top1": top5_results[0], "top5": top5_results,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "image_name": uploaded_file.name,
                        "boxes": boxes, "labels": labels, "confidences": confidences
                    }
                    st.rerun()
    
    with col2:
        st.markdown("### 📋 诊断结果")
        
        if st.session_state.get("current_diagnosis"):
            diagnosis = st.session_state["current_diagnosis"]
            top1 = diagnosis["top1"]
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E88E5 0%, #00ACC1 100%); 
                        padding: 24px; border-radius: 16px; color: white; text-align: center; margin: 20px 0;
                        box-shadow: 0 4px 16px rgba(30, 136, 229, 0.3);">
                <h2 style="margin: 0; color: white !important;">{top1['class']}</h2>
                <p style="font-size: 14px; opacity: 0.9; margin: 5px 0 0 0;">{top1['class_en']}</p>
                <h1 style="font-size: 42px; margin: 15px 0 0 0; color: white !important;">{top1['probability']:.1%}</h1>
                <p style="font-size: 12px; opacity: 0.8; margin: 5px 0 0 0;">置信度</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**使用模型:** `{diagnosis['model_used']}` | **时间:** {diagnosis['timestamp']}")
            
            st.markdown("### 📊 Top-5 概率分布")
            for i, item in enumerate(diagnosis["top5"]):
                prob = item["probability"]
                st.markdown(f"**{i+1}. {item['class']}** - {prob:.2%}")
                st.progress(prob)
            
            st.markdown("### 💡 诊断建议")
            st.info("建议到皮肤科进行专业检查。避免抓挠患处，保持皮肤湿润，减少精神压力。")
            
            if st.button("💾 保存诊断记录", use_container_width=True):
                record = {"id": len(st.session_state["diagnosis_records"]) + 1, **diagnosis}
                st.session_state["diagnosis_records"].append(record)
                st.success("诊断记录已保存!")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px; background: white; border-radius: 16px; border: 2px dashed #CBD5E1;">
                <p style="font-size: 48px; margin: 0;">📷</p>
                <p style="color: #475569;">请上传皮肤病变图像</p>
            </div>
            """, unsafe_allow_html=True)


def page_chat():
    """智能对话页面"""
    st.title("💬 智能对话")
    st.markdown("基于RAG知识库与大语言模型的AI医生助手")
    
    # 快捷问题
    quick_questions = ["脸上长痘痘怎么办？", "湿疹怎么护理？", "银屑病有哪些症状？", "荨麻疹怎么引起的？"]
    cols = st.columns(4)
    for i, q in enumerate(quick_questions):
        if cols[i].button(q, key=f"quick_{i}_{len(st.session_state['chat_messages'])}"):
            # 生成回复
            responses = {
                "脸上长痘痘怎么办？": """关于痤疮（青春痘）：

**常见原因：**
- 皮脂分泌旺盛，毛孔堵塞
- 细菌感染
- 激素水平变化

**护理建议：**
1. 每天用温和的洁面产品清洁面部2次
2. 不要用手挤压痘痘，以免留下疤痕
3. 选择非致痘的护肤品
4. 规律作息，减少熬夜

**饮食建议：**
- 少吃辛辣、油腻、甜食
- 多吃蔬菜水果

⚠️ 如痘痘严重或持续不退，建议就医皮肤科。""",
                
                "湿疹怎么护理？": """关于湿疹：

**常见症状：**
- 皮肤红斑、丘疹
- 剧烈瘙痒
- 皮肤干燥、脱屑

**护理建议：**
1. 保持皮肤湿润，使用保湿霜
2. 避免过热的水洗澡
3. 穿棉质宽松衣物
4. 避免抓挠患处

⚠️ 建议就医确诊类型并接受针对性治疗。""",
                
                "银屑病有哪些症状？": """关于银屑病（牛皮癣）：

**典型特征：**
- 红色斑块覆盖银白色鳞屑
- 薄膜现象（刮除鳞屑后可见薄膜）
- 点状出血
- 好发于头皮、肘部、膝盖

**诱发因素：**
- 感染
- 精神压力
- 外伤
- 吸烟、饮酒

⚠️ 请到正规医院皮肤科就诊。""",
                
                "荨麻疹怎么引起的？": """关于荨麻疹（风团）：

**典型特征：**
- 红色或苍白色风团
- 剧烈瘙痒
- 来去迅速（24小时内消退）

**常见诱因：**
- 食物过敏（海鲜、坚果等）
- 药物过敏
- 感染
- 物理刺激（冷、热、压力）

⚠️ 如出现呼吸困难，请立即就医！"""
            }
            
            # 清空并重新开始对话
            st.session_state["chat_messages"] = [
                {"role": "user", "content": q},
                {"role": "assistant", "content": responses.get(q, "建议咨询专业医生。")}
            ]
            st.rerun()
    
    st.markdown("---")
    
    # 对话记录 - 医疗风格气泡
    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background: #1E88E5; color: white !important; padding: 12px 16px; 
                        border-radius: 18px 18px 4px 18px; margin: 8px 0; max-width: 80%; margin-left: auto;">
                <p style="color: white !important; margin: 0; font-weight: 600;">👤 您</p>
                <p style="color: white !important; margin: 5px 0 0 0;">{msg['content']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #E2E8F0; padding: 12px 16px; 
                        border-radius: 18px 18px 18px 4px; margin: 8px 0; max-width: 80%;">
                <p style="color: #1E88E5 !important; margin: 0; font-weight: 600;">🏥 AI医生</p>
                <div style="color: #475569 !important; margin: 5px 0 0 0; white-space: pre-wrap;">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # 输入框 - 使用 form 避免重复提交
    with st.form("chat_form"):
        user_input = st.text_input("请描述您的皮肤问题...", key="chat_input_main")
        submit = st.form_submit_button("发送", type="primary")
        
        if submit and user_input:
            # 添加用户消息和AI回复
            st.session_state["chat_messages"].append({"role": "user", "content": user_input})
            response = f"""感谢您的咨询！

根据您描述的：{user_input}

**一般性建议：**
1. 保持患处清洁干燥
2. 避免使用刺激性护肤品
3. 观察症状变化
4. 如有加重及时就医

⚠️ 本回答仅供参考，不作为正式医疗诊断。如症状持续或加重，请尽快就医。"""
            st.session_state["chat_messages"].append({"role": "assistant", "content": response})
            st.rerun()
    
    # 清空对话按钮
    if st.button("🗑️ 清空对话"):
        st.session_state["chat_messages"] = [{"role": "assistant", "content": "您好！我是皮肤病智能诊断助手。请描述您遇到的皮肤问题？"}]
        st.rerun()


def page_advice():
    """预防建议页面"""
    st.title("🛡️ 预防建议")
    st.markdown("专业皮肤病预防知识和日常护理指南")
    
    search = st.text_input("🔍 搜索疾病", placeholder="输入疾病名称...")
    
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
            "护理": ["冷敷缓解", "避免抓挠", "备好抗组胺药"]
        },
        "特应性皮炎": {
            "预防": ["保持皮肤湿润", "避免过敏原", "减少精神压力", "注意饮食"],
            "饮食": ["避免致敏食物", "补充维生素D", "少吃辛辣"],
            "护理": ["使用温和洗护", "坚持保湿", "避免过热洗澡"]
        },
        "脂溢性皮炎": {
            "预防": ["规律作息", "减少压力", "避免刺激性护肤品"],
            "饮食": ["少吃辛辣油腻", "补充维生素B", "戒酒"],
            "护理": ["使用温和洁面", "保持皮肤清爽", "避免抓挠"]
        },
        "白癜风": {
            "预防": ["避免外伤", "减少精神压力", "注意防晒"],
            "饮食": ["补充微量元素", "多吃黑色食物", "补充维生素C"],
            "护理": ["避免暴晒", "保护皮肤", "保持心情愉悦"]
        },
        "带状疱疹": {
            "预防": ["提高免疫力", "避免过度劳累", "接种疫苗"],
            "饮食": ["清淡饮食", "补充蛋白质", "避免辛辣"],
            "护理": ["保持患处清洁", "避免抓挠", "及时就医"]
        },
        "单纯疱疹": {
            "预防": ["避免诱发因素", "增强免疫力", "避免与患者接触"],
            "饮食": ["清淡饮食", "补充维生素", "避免刺激性食物"],
            "护理": ["保持唇部清洁", "避免挤压", "使用抗病毒药膏"]
        },
        "手足癣": {
            "预防": ["保持手足干燥", "穿透气鞋子", "不共用拖鞋"],
            "饮食": ["均衡饮食", "补充维生素B", "增强免疫力"],
            "护理": ["每天更换袜子", "保持脚部干燥", "定期消毒鞋子"]
        },
        "甲癣": {
            "预防": ["保持手足清洁", "避免共用修甲工具", "治疗足癣"],
            "饮食": ["均衡营养", "补充蛋白质", "增强免疫力"],
            "护理": ["定期修剪指甲", "保持干燥", "避免外伤"]
        },
        "扁平疣": {
            "预防": ["避免直接接触", "增强免疫力", "避免皮肤破损"],
            "饮食": ["均衡饮食", "补充维生素", "提高免疫力"],
            "护理": ["避免抓挠", "保持皮肤清洁", "及时就医"]
        },
        "玫瑰痤疮": {
            "预防": ["避免刺激因素", "减少日晒", "忌饮酒"],
            "饮食": ["避免辛辣刺激", "少吃热饮", "补充维生素"],
            "护理": ["温和护肤", "避免过度清洁", "注意防晒"]
        },
        "皮肤瘙痒症": {
            "预防": ["保持皮肤湿润", "避免过度清洗", "注意衣物材质"],
            "饮食": ["清淡饮食", "补充水分", "避免辛辣"],
            "护理": ["保持皮肤湿润", "避免抓挠", "使用温和洗护"]
        },
        "血管瘤": {
            "预防": ["孕期保健", "避免外伤", "定期检查"],
            "饮食": ["均衡营养", "补充维生素", "增强体质"],
            "护理": ["避免摩擦", "观察变化", "及时就医"]
        },
        "脂溢性角化病": {
            "预防": ["避免长期日晒", "保护皮肤", "定期检查"],
            "饮食": ["抗氧化食物", "补充维生素", "清淡饮食"],
            "护理": ["避免摩擦", "观察变化", "就医咨询"]
        },
        "黑色素瘤": {
            "预防": ["避免过度日晒", "定期自查", "警惕痣的变化"],
            "饮食": ["抗氧化饮食", "补充维生素D", "少吃加工食品"],
            "护理": ["ABCDE自检", "及时就医", "避免刺激"]
        },
        "基底细胞癌": {
            "预防": ["避免过度日晒", "使用防晒", "定期检查"],
            "饮食": ["抗氧化食物", "健康饮食", "补充维生素"],
            "护理": ["观察皮损变化", "避免外伤", "及时就医"]
        },
        "系统性红斑狼疮": {
            "预防": ["避免日晒", "预防感染", "规律作息"],
            "饮食": ["均衡饮食", "补充钙质", "避免光敏食物"],
            "护理": ["避免日晒", "预防感染", "定期复查"]
        },
        "皮肌炎": {
            "预防": ["增强免疫力", "避免感染", "定期体检"],
            "饮食": ["高蛋白饮食", "补充维生素", "避免刺激性食物"],
            "护理": ["观察肌力变化", "预防感染", "定期复查"]
        },
        "硬皮病": {
            "预防": ["避免外伤", "戒烟", "注意保暖"],
            "饮食": ["高蛋白饮食", "补充维生素", "清淡饮食"],
            "护理": ["皮肤护理", "功能锻炼", "定期复查"]
        },
        "天疱疮": {
            "预防": ["增强免疫力", "避免感染", "定期体检"],
            "饮食": ["高蛋白饮食", "补充维生素", "避免刺激性食物"],
            "护理": ["保护皮肤", "预防感染", "遵医嘱用药"]
        },
        "疥疮": {
            "预防": ["避免接触患者", "注意个人卫生", "勤换衣物"],
            "饮食": ["均衡饮食", "增强免疫力", "清淡饮食"],
            "护理": ["彻底治疗", "消毒衣物", "避免抓挠"]
        }
    }
    
    diseases = list(advice_data.keys())
    selected = st.selectbox("选择疾病", diseases if not search else [d for d in diseases if search in d])
    
    if selected:
        d = advice_data[selected]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🛡️ 预防措施")
            for x in d["预防"]:
                st.write(f"- {x}")
        with col2:
            st.markdown("### 🍽️ 饮食建议")
            for x in d["饮食"]:
                st.write(f"- {x}")
        with col3:
            st.markdown("### 💆 日常护理")
            for x in d["护理"]:
                st.write(f"- {x}")


def page_history():
    """历史记录页面"""
    st.title("📋 诊断历史")
    st.markdown("查看和管理您的历史诊断记录")
    
    records = st.session_state["diagnosis_records"]
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("总诊断次数", len(records))
    with col2: st.metric("最近诊断", records[0]["timestamp"] if records else "暂无")
    with col3: st.metric("平均置信度", f"{sum(r['confidence'] for r in records)/len(records):.1%}" if records else "0%")
    
    st.markdown("---")
    
    for record in records:
        conf = record["confidence"]
        color = "#2E7D32" if conf >= 0.8 else "#F9A825"
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 16px; margin: 12px 0; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #E2E8F0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: #1E293B !important;">{record['disease']}</h3>
                    <p style="margin: 5px 0 0 0; color: #475569; font-size: 12px;">{record['disease_en']} | {record['timestamp']}</p>
                </div>
                <div style="background: {color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600;">
                    {conf:.1%}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def page_profile():
    """用户中心页面"""
    st.title("👤 用户中心")
    st.markdown("管理您的个人信息和诊断偏好")
    
    user = st.session_state["user_info"]
    
    tab1, tab2, tab3 = st.tabs(["👤 基本信息", "⚙️ 偏好设置", "📊 数据管理"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("昵称", value=user.get("name", ""))
            new_email = st.text_input("邮箱", value=user.get("email", ""))
        with col2:
            new_phone = st.text_input("电话", value=user.get("phone", ""))
            new_age = st.number_input("年龄", value=user.get("age", 25), min_value=0, max_value=120)
        
        if st.button("💾 保存修改", type="primary"):
            user["name"] = new_name
            user["email"] = new_email
            user["phone"] = new_phone
            user["age"] = new_age
            st.session_state["user_info"] = user
            st.success("信息已保存!")
    
    with tab2:
        theme = st.radio("主题", ["☀️ 浅色模式", "🌙 深色模式"], index=0)
        lang = st.radio("语言", ["中文", "English"], index=0)
        if st.button("⚙️ 保存偏好"):
            st.success("偏好已保存!")
    
    with tab3:
        st.metric("诊断记录", len(st.session_state["diagnosis_records"]))
        if st.button("🗑️ 清空数据"):
            st.session_state["diagnosis_records"] = []
            st.rerun()


# ============ 侧边栏导航 ============

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #1890ff; margin: 0;">🏥 MedSkin</h2>
        <p style="color: #666; font-size: 12px;">皮肤病智能诊断</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 导航菜单
    pages = {"诊断分析": "📊", "智能对话": "💬", "预防建议": "🛡️", "历史记录": "📋", "用户中心": "👤"}
    selected = st.radio("导航", list(pages.keys()), format_func=lambda x: f"{pages[x]} {x}")
    st.session_state["current_page"] = selected
    
    st.markdown("---")
    
    with st.expander("⚙️ 设置"):
        st.selectbox("语言", ["中文", "English"], index=0)
        st.caption("v2.0.0")
    
    # 用户信息显示
    st.markdown(f"""
    <div style="background: #F8FAFC; 
                padding: 16px; border-radius: 12px; text-align: center; margin-bottom: 10px;
                border: 1px solid #E2E8F0;">
        <p style="color: #1E88E5; margin: 0; font-weight: 600; font-size: 15px;">
            👤 {st.session_state['username']}
        </p>
        <p style="color: #2E7D32; font-size: 11px; margin: 5px 0 0 0;">
            ● 已登录
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state["is_logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["user_info"]["name"] = "访客用户"
        st.rerun()


# ============ 显示当前页面 ============

if st.session_state["current_page"] == "诊断分析":
    page_diagnosis()
elif st.session_state["current_page"] == "智能对话":
    page_chat()
elif st.session_state["current_page"] == "预防建议":
    page_advice()
elif st.session_state["current_page"] == "历史记录":
    page_history()
elif st.session_state["current_page"] == "用户中心":
    page_profile()
