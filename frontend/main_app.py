"""
streamlit主入口页面
"""

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="皮肤病智能诊断系统",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

SKIN_DISEASES = [
    ("痤疮与酒渣鼻", "Acne and Rosacea Photos"),
    ("光化性角化病与基底细胞癌", "Actinic Keratosis Basal Cell Carcinoma"),
    ("特应性皮炎", "Atopic Dermatitis Photos"),
    ("大疱性疾病", "Bullous Disease Photos"),
    ("蜂窝织炎与脓疱病", "Cellulitis Impetigo and other Bacterial Infections"),
    ("湿疹", "Eczema Photos"),
    ("皮疹与药物反应", "Exanthems and Drug Eruptions"),
    ("脱发", "Hair Loss Photos Alopecia"),
    ("疱疹、HPV及其他性病", "Herpes HPV and other STDs Photos"),
    ("色素性疾病", "Light Diseases and Disorders of Pigmentation"),
    ("狼疮及结缔组织病", "Lupus and other Connective Tissue diseases"),
    ("黑色素瘤、皮肤癌与痣", "Melanoma Skin Cancer Nevi and Moles"),
    ("指甲疾病", "Nail Fungus and other Nail Disease"),
    ("毒葛皮炎", "Poison Ivy Photos and other Contact Dermatitis"),
    ("银屑病与扁平苔藓", "Psoriasis pictures Lichen Planus"),
    ("疥疮、莱姆病及寄生虫感染", "Scabies Lyme Disease and other Infestations"),
    ("脂溢性角化病及良性肿瘤", "Seborrheic Keratoses and other Benign Tumors"),
    ("系统性疾病", "Systemic Disease"),
    ("真菌感染", "Tinea Ringworm Candidiasis and other Fungal Infections"),
    ("荨麻疹", "Urticaria Hives"),
    ("血管瘤", "Vascular Tumors"),
    ("血管炎", "Vasculitis Photos"),
    ("疣、传染性软疣及病毒感染", "Warts Molluscum and other Viral Infections"),
]

if "theme" not in st.session_state:
    st.session_state["theme"] = "light"
if "language" not in st.session_state:
    st.session_state["language"] = "中文"
if "user_info" not in st.session_state:
    st.session_state["user_info"] = {
        "name": "访客用户",
        "email": "",
        "history_count": 0
    }
if "diagnosis_count" not in st.session_state:
    st.session_state["diagnosis_count"] = 0
if "accuracy" not in st.session_state:
    st.session_state["accuracy"] = 0.0
if "last_diagnosis_time" not in st.session_state:
    st.session_state["last_diagnosis_time"] = None

def apply_theme():
    if st.session_state["theme"] == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .css-1d391kg { background-color: #161b22; }
        .css-1nc3unp { background-color: #21262d; }
        .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; }
        .stTextInput>div>div>input { background-color: #21262d; color: #c9d1d9; border-color: #30363d; }
        .stTextArea>div>div>textarea { background-color: #21262d; color: #c9d1d9; border-color: #30363d; }
        div[data-testid="stExpander"] { background-color: #161b22; border: 1px solid #30363d; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; }
        .css-1d391kg { background-color: #ffffff; }
        .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; }
        </style>
        """, unsafe_allow_html=True)

def get_text(key):
    texts = {
        "zh": {
            "welcome": "欢迎使用皮肤病智能诊断系统",
            "subtitle": "AI驱动的皮肤病辅助诊断平台",
            "features": "核心功能",
            "image_analysis": "图片上传与分析",
            "image_desc": "上传皮肤图片，AI实时分析皮肤病症状",
            "chat": "智能对话",
            "chat_desc": "与AI助手对话，详细描述您的症状",
            "history": "诊断历史",
            "history_desc": "查看历史诊断记录和分析报告",
            "prevention": "预防建议",
            "prevention_desc": "获取专业皮肤病预防和护理建议",
            "user_center": "用户中心",
            "user_desc": "管理个人信息和诊断偏好",
            "quick_stats": "快速统计",
            "total_diagnoses": "总诊断次数",
            "accuracy": "诊断准确率",
            "supported_diseases": "支持疾病类型",
            "last_diagnosis": "最近诊断",
            "latest_news": "最新功能更新",
            "click_to_view": "点击查看疾病列表"
        },
        "en": {
            "welcome": "Welcome to Skin Disease Diagnosis System",
            "subtitle": "AI-Powered Skin Disease Auxiliary Diagnosis Platform",
            "features": "Core Features",
            "image_analysis": "Image Upload & Analysis",
            "image_desc": "Upload skin images, AI analyzes symptoms in real-time",
            "chat": "Smart Chat",
            "chat_desc": "Chat with AI assistant about your symptoms",
            "history": "Diagnosis History",
            "history_desc": "View historical diagnosis records and reports",
            "prevention": "Prevention Tips",
            "prevention_desc": "Get professional skin disease prevention advice",
            "user_center": "User Center",
            "user_desc": "Manage personal info and diagnosis preferences",
            "quick_stats": "Quick Stats",
            "total_diagnoses": "Total Diagnoses",
            "accuracy": "Accuracy Rate",
            "supported_diseases": "Supported Diseases",
            "last_diagnosis": "Last Diagnosis",
            "latest_news": "Latest Updates",
            "click_to_view": "Click to view disease list"
        }
    }
    return texts.get(st.session_state.language, texts["zh"]).get(key, key)

def get_last_diagnosis_display():
    if st.session_state["last_diagnosis_time"]:
        return st.session_state["last_diagnosis_time"]
    return "暂无"

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #667eea;"> MedSkin</h2>
        <p style="color: #888; font-size: 12px;">皮肤病智能诊断</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.expander(" 设置", expanded=True):
        theme_options = ["light", "dark"]
        theme_labels = {"light": " 浅色模式", "dark": " 深色模式"}
        selected_theme = st.selectbox(
            "主题模式",
            theme_options,
            index=theme_options.index(st.session_state["theme"]),
            format_func=lambda x: theme_labels[x],
            key="theme_selector"
        )
        if selected_theme != st.session_state["theme"]:
            st.session_state["theme"] = selected_theme
            st.rerun()
        
        lang_options = ["中文", "English"]
        selected_lang = st.selectbox(
            "语言",
            lang_options,
            index=lang_options.index(st.session_state["language"]) if st.session_state["language"] in lang_options else 0,
            key="lang_selector"
        )
        if selected_lang != st.session_state["language"]:
            st.session_state["language"] = selected_lang
            st.rerun()
    
    st.markdown("---")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; border-radius: 10px; text-align: center;">
        <p style="color: white; margin: 0;"> {st.session_state['user_info']['name']}</p>
        <p style="color: rgba(255,255,255,0.8); font-size: 11px; margin: 5px 0 0 0;">
             {st.session_state['user_info']['email'] or '未设置邮箱'}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

apply_theme()

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 42px; margin-bottom: 10px;">
             {get_text('welcome')}
        </h1>
        <p style="color: #666; font-size: 18px;">{get_text('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.subheader(get_text('quick_stats'))
stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.metric(f" {get_text('total_diagnoses')}", st.session_state["diagnosis_count"], "↑ 1")
with stats_col2:
    st.metric(f" {get_text('accuracy')}", f"{st.session_state['accuracy']:.1f}%" if st.session_state["accuracy"] > 0 else "--", "+0.5%")
with stats_col3:
    disease_count = len(SKIN_DISEASES)
    st.metric(f" {get_text('supported_diseases')}", disease_count)
    with st.expander(f" {get_text('click_to_view')}"):
        for i, (cn_name, en_name) in enumerate(SKIN_DISEASES, 1):
            st.write(f"{i}. {cn_name} ({en_name})")
with stats_col4:
    st.metric(f" {get_text('last_diagnosis')}", get_last_diagnosis_display())

st.markdown("---")

st.subheader(get_text('features'))
feature_cols = st.columns(4)

features = [
    ("", get_text('image_analysis'), get_text('image_desc'), "诊断分析"),
    ("", get_text('chat'), get_text('chat_desc'), "智能对话"),
    ("", get_text('history'), get_text('history_desc'), "历史记录"),
    ("️", get_text('prevention'), get_text('prevention_desc'), "预防建议"),
]

for i, (icon, title, desc, page) in enumerate(features):
    with feature_cols[i]:
        st.markdown(f"""
        <div style="background: white; padding: 25px; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;
                    transition: transform 0.3s; cursor: pointer;">
            <h2 style="font-size: 50px; margin: 0;">{icon}</h2>
            <h4 style="color: #333; margin: 15px 0 10px 0;">{title}</h4>
            <p style="color: #666; font-size: 13px;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"进入 →", key=f"goto_{page}"):
            st.switch_page(f"pages/{page}.py")

st.markdown("---")

st.subheader(get_text('latest_news'))
with st.expander("多图对比功能", expanded=True):
    st.success(" 支持同时上传多张图片进行对比分析")
    st.success(" 新增进度指示器，实时显示诊断步骤")
    st.success(" 支持中英文切换")

with st.expander("UI界面"):
    st.info(" 现代化科技风格设计")
    st.info(" 支持深色模式切换")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 20px;">
    <p>© 2026 MedSkin 皮肤病智能诊断系统 | 技术支持: AI Agent</p>
</div>
""", unsafe_allow_html=True)
