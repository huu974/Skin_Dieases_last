"""
用户信息管理
"""

import streamlit as st

st.set_page_config(page_title="用户中心", page_icon="", layout="wide")

def apply_theme():
    if st.session_state.get("theme", "light") == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

st.title(" 用户中心")
st.markdown("管理您的个人信息和诊断偏好")

if "user_info" not in st.session_state:
    st.session_state["user_info"] = {
        "name": "访客用户",
        "email": "",
        "phone": "",
        "age": "",
        "gender": "未设置",
        "skin_type": "普通",
        "allergies": "",
        "notifications": True
    }

if "phone" not in st.session_state["user_info"]:
    st.session_state["user_info"]["phone"] = ""
if "age" not in st.session_state["user_info"]:
    st.session_state["user_info"]["age"] = ""

if "saved" not in st.session_state:
    st.session_state["saved"] = False

tab1, tab2, tab3 = st.tabs([" 基本信息", " 偏好设置", " 通知管理"])

with tab1:
    st.markdown("### 基本信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("姓名", value=st.session_state["user_info"]["name"])
        email = st.text_input("邮箱", value=st.session_state["user_info"]["email"])
        phone = st.text_input("电话", value=st.session_state["user_info"]["phone"])
    
    with col2:
        age_value = st.session_state["user_info"].get("age", "")
        age_default = int(age_value) if age_value and age_value.isdigit() else 25
        age = st.number_input("年龄", min_value=0, max_value=120, value=age_default)
        gender = st.selectbox(
            "性别",
            ["男", "女", "其他", "未设置"],
            index=["男", "女", "其他", "未设置"].index(st.session_state["user_info"]["gender"]) if st.session_state["user_info"]["gender"] in ["男", "女", "其他", "未设置"] else 3
        )
    
    st.markdown("### 健康信息")
    
    col3, col4 = st.columns(2)
    
    with col3:
        skin_type = st.selectbox(
            "皮肤类型",
            ["干性", "油性", "混合性", "敏感性", "普通"],
            index=["干性", "油性", "混合性", "敏感性", "普通"].index(st.session_state["user_info"]["skin_type"]) if st.session_state["user_info"]["skin_type"] in ["干性", "油性", "混合性", "敏感性", "普通"] else 4
        )
    
    with col4:
        allergies = st.text_input("过敏史", value=st.session_state["user_info"]["allergies"], placeholder="如：海鲜、青霉素等")
    
    col_btn, _, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button(" 保存修改", type="primary", use_container_width=True):
            st.session_state["user_info"]["name"] = name
            st.session_state["user_info"]["email"] = email
            st.session_state["user_info"]["phone"] = phone
            st.session_state["user_info"]["age"] = age
            st.session_state["user_info"]["gender"] = gender
            st.session_state["user_info"]["skin_type"] = skin_type
            st.session_state["user_info"]["allergies"] = allergies
            st.session_state["saved"] = True
            st.success(" 信息已保存!")
    
    if st.session_state.get("saved"):
        st.balloons()

with tab2:
    st.markdown("### 诊断偏好设置")
    
    st.markdown("####  语言设置")
    lang = st.radio(
        "选择语言",
        ["中文", "English"],
        index=0 if st.session_state.get("language") == "中文" else 1,
        horizontal=True
    )
    if lang != st.session_state.get("language"):
        st.session_state["language"] = lang
        st.rerun()
    
    st.markdown("####  界面主题")
    theme = st.radio(
        "选择主题",
        [" 浅色模式", " 深色模式"],
        index=0 if st.session_state.get("theme", "light") == "light" else 1,
        horizontal=True
    )
    if theme == " 浅色模式" and st.session_state.get("theme") != "light":
        st.session_state["theme"] = "light"
        st.rerun()
    elif theme == " 深色模式" and st.session_state.get("theme") != "dark":
        st.session_state["theme"] = "dark"
        st.rerun()
    
    st.markdown("####  AI诊断设置")
    
    confidence_threshold = st.slider(
        "置信度阈值",
        min_value=50,
        max_value=99,
        value=80,
        help="只显示置信度高于此值的诊断结果"
    )
    
    auto_analyze = st.checkbox("自动分析上传的图片", value=True)
    
    show_similar = st.checkbox("显示相似病例参考", value=True)
    
    if st.button(" 保存偏好设置"):
        st.success("偏好设置已保存!")

with tab3:
    st.markdown("### 通知设置")
    
    notifications = st.toggle("启用通知", value=st.session_state["user_info"].get("notifications", True))
    
    st.markdown("####  通知类型")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("诊断结果通知", value=True)
        st.checkbox("复诊提醒", value=True)
    
    with col2:
        st.checkbox("健康资讯推送", value=False)
        st.checkbox("系统更新公告", value=True)
    
    st.markdown("---")
    
    st.markdown("###  联系方式订阅")
    
    col3, col4 = st.columns([3, 1])
    with col3:
        email_for_notif = st.text_input("订阅邮箱", value=st.session_state["user_info"]["email"], placeholder="输入邮箱订阅健康提醒")
    with col4:
        st.button("订阅", use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("###  数据管理")
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        st.button(" 导出我的数据", use_container_width=True)
    
    with col_btn2:
        st.button(" 同步云端", use_container_width=True)
    
    with col_btn3:
        st.button(" 清空本地数据", use_container_width=True)

# st.markdown("---")
#
# st.markdown("""
# <div style="text-align: center; color: #999; padding: 20px;">
#     <p>© 2026 MedSkin 皮肤病智能诊断系统 | 版本 v2.1.0</p>
#     <p>如有疑问，请联系 support@medskin.com</p>
# </div>
# """, unsafe_allow_html=True)
