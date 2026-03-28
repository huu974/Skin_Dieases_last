"""
预防建议页面
"""

import streamlit as st

st.set_page_config(page_title="预防建议", page_icon="🛡", layout="wide")

def apply_theme():
    if st.session_state.get("theme", "light") == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

st.title(" 预防建议")
st.markdown("专业皮肤病预防和日常护理指南")

categories = {
    " 日常防护": {
        "icon": "",
        "tips": [
            "避免长时间暴露在阳光下，外出时使用防晒霜",
            "保持皮肤清洁，每天洗澡但避免过热的水",
            "选择温和无刺激的护肤品和沐浴产品",
            "保持充足的睡眠，增强免疫力"
        ]
    },
    " 饮食调理": {
        "icon": "",
        "tips": [
            "多吃新鲜蔬菜水果，补充维生素",
            "避免辛辣、油腻、刺激性食物",
            "戒烟限酒，减少对皮肤的刺激",
            "保持充足的水分摄入"
        ]
    },
    " 生活习惯": {
        "icon": "",
        "tips": [
            "规律作息，避免熬夜",
            "适当运动，增强体质",
            "学会减压，保持心情愉悦",
            "穿着宽松透气的棉质衣物"
        ]
    },
    " 定期检查": {
        "icon": "",
        "tips": [
            "定期进行皮肤自查",
            "发现问题及时就医",
            "遵医嘱用药，不擅自停药",
            "记录皮肤变化，便于医生诊断"
        ]
    }
}

tabs = st.tabs(list(categories.keys()))

for tab, (category, data) in zip(tabs, categories.items()):
    with tab:
        st.markdown(f"### {data['icon']} {category.replace(data['icon'], '').strip()}")
        
        for i, tip in enumerate(data["tips"]):
            with st.container():
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                width: 40px; height: 40px; border-radius: 50%; 
                                display: flex; align-items: center; justify-content: center;
                                color: white; font-weight: bold;">
                        {i+1}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background: white; padding: 15px; border-radius: 10px;
                                border-left: 4px solid #667eea; margin: 5px 0;">
                        <p style="margin: 0; color: #333;">{tip}</p>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("---")

st.subheader(" 常见皮肤病预防")

diseases = {
    "银屑病": {
        "预防": ["避免感染", "减少精神压力", "戒烟戒酒", "避免外伤"],
        "饮食": ["多吃蔬果", "补充Omega-3", "少吃牛羊肉"]
    },
    "湿疹": {
        "预防": ["保持皮肤湿润", "避免接触过敏原", "穿棉质衣物", "适度洗澡"],
        "饮食": ["避免海鲜", "少吃辛辣", "补充维生素C"]
    },
    "痤疮": {
        "预防": ["清洁面部", "不挤压痘痘", "规律作息", "卸妆彻底"],
        "饮食": ["少吃甜食", "避免油炸", "多喝水"]
    },
    "荨麻疹": {
        "预防": ["查找过敏原", "避免冷热刺激", "穿着宽松", "保持清洁"],
        "饮食": ["记录食物日记", "避免已知的过敏食物"]
    }
}

disease_tabs = st.tabs(list(diseases.keys()))

for tab, (disease, info) in zip(disease_tabs, diseases.items()):
    with tab:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("####  预防措施")
            for tip in info["预防"]:
                st.write(f"• {tip}")
        with col2:
            st.markdown("####  饮食建议")
            for tip in info["饮食"]:
                st.write(f"• {tip}")

# st.markdown("---")

# with st.expander(" 更多资源"):
#     st.markdown("""
#     ### 权威资源链接
#     - [中华皮肤科协会](https://www.cda.org.cn)
#     - [世界卫生组织皮肤健康](https://www.who.int/health-topics/skin-diseases)
#     - [美国皮肤病学会](https://www.aad.org)
#     """)
