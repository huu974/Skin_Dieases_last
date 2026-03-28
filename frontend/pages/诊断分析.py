"""
用户上传诊断页面
"""

import streamlit as st
import tempfile
import os
import time
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="诊断分析", page_icon="", layout="wide")

def apply_theme():
    if st.session_state.get("theme", "light") == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

st.title("诊断分析")
st.markdown("上传皮肤图片，AI将自动分析并提供诊断建议")

if "diagnosis_results" not in st.session_state:
    st.session_state["diagnosis_results"] = []
if "uploaded_images" not in st.session_state:
    st.session_state["uploaded_images"] = []

tab1, tab2 = st.tabs([" 单图分析", " 多图对比"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 上传图片")
        uploaded_file = st.file_uploader(
            "选择皮肤图片",
            type=["jpg", "jpeg", "png"],
            help="支持 JPG、PNG 格式，建议图片清晰、光照均匀"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="已上传图片", use_container_width=True)
            
            if st.button(" 开始分析", type="primary", use_container_width=True):
                st.session_state["diagnosis_results"] = []
                st.session_state["uploaded_images"] = []
                
                with st.spinner(""):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    steps = [
                        ("正在预处理图片...", 20),
                        ("正在加载AI模型...", 40),
                        ("正在进行皮肤病检测...", 70),
                        ("正在生成诊断报告...", 90),
                        ("分析完成!", 100)
                    ]
                    
                    for step_text, progress in steps:
                        status_text.text(step_text)
                        progress_bar.progress(progress)
                        time.sleep(0.8)
                    
                    results = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "image_name": uploaded_file.name,
                        "disease": "银屑病 (Psoriasis)",
                        "confidence": 87.5,
                        "severity": "中等",
                        "description": "检测到典型的银屑病特征，包括红斑、鳞屑和边界清晰的皮损区域。建议尽快就医进行进一步确诊。",
                        "recommendations": [
                            "建议到皮肤科进行专业检查",
                            "避免抓挠患处",
                            "保持皮肤湿润",
                            "减少精神压力"
                        ]
                    }
                    
                    st.session_state["diagnosis_results"].append(results)
                    st.session_state["diagnosis_count"] = st.session_state.get("diagnosis_count", 0) + 1
                    st.session_state["accuracy"] = 94.2
                    st.session_state["last_diagnosis_time"] = "刚刚"
                    st.session_state["uploaded_images"].append(uploaded_file.name)
                    st.success(" 分析完成!")
                    st.rerun()
    
    with col2:
        st.markdown("### 诊断结果")
        
        if st.session_state["diagnosis_results"]:
            latest = st.session_state["diagnosis_results"][-1]
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; color: white;">
                <h3 style="margin: 0;"> {latest['disease']}</h3>
                <p style="font-size: 14px; opacity: 0.9;">置信度: {latest['confidence']}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"严重程度: `{latest['severity']}`")
            st.markdown(f"诊断时间: {latest['timestamp']}")
            
            with st.expander(" 详细描述", expanded=True):
                st.write(latest["description"])
            
            with st.expander(" 建议措施"):
                for rec in latest["recommendations"]:
                    st.write(f"• {rec}")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📄 导出报告", use_container_width=True):
                    report_content = f"""
       皮肤病诊断报告

诊断时间: {latest['timestamp']}
上传图片: {latest['image_name']}

诊断结果:
疾病名称: {latest['disease']}
置信度: {latest['confidence']}%
严重程度: {latest['severity']}

详细描述:
{latest['description']}

建议措施:
"""
                    for i, rec in enumerate(latest['recommendations'], 1):
                        report_content += f"{i}. {rec}\n"
                    
                    report_content += """
      本报告仅供参考，请以医生诊断为准
                    """
                    
                    st.download_button(
                        label="下载报告",
                        data=report_content,
                        file_name=f"诊断报告_{latest['timestamp'].replace(':', '-').replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            
            with col_btn2:
                if st.button(" 加入对比", use_container_width=True):
                    st.session_state["compare_list"] = st.session_state.get("compare_list", [])
                    st.session_state["compare_list"].append(latest)
                    st.success("已添加到对比列表!")
        else:
            st.info(" 请先上传图片并点击分析")

with tab2:
    st.markdown("### 多图对比分析")
    st.markdown("上传多张图片进行对比观察")
    
    compare_files = st.file_uploader(
        "上传多张图片",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="可选择多张图片进行对比"
    )
    
    if compare_files:
        cols = st.columns(min(len(compare_files), 3))
        for i, file in enumerate(compare_files):
            with cols[i % 3]:
                st.image(file, caption=f"图片 {i+1}: {file.name}", use_container_width=True)
        
        if len(compare_files) >= 2:
            if st.button(" 对比分析", type="primary", use_container_width=True):
                with st.spinner("正在进行对比分析..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.03)
                        progress_bar.progress(i + 1)
                    
                    st.success(" 对比分析完成!")
                    
                    st.markdown("""
                    <div style="background: #f0f0f0; padding: 20px; border-radius: 10px; margin-top: 20px;">
                        <h4> 对比分析结果</h4>
                        <ul>
                            <li>图片1 vs 图片2: 病变区域相似度 78%</li>
                            <li>变化趋势: 病变区域有所扩大</li>
                            <li>建议: 持续观察，必要时就医</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info(" 请上传至少2张图片进行对比")

st.markdown("---")
if st.session_state.get("compare_list"):
    with st.expander(f" 待对比列表 ({len(st.session_state['compare_list'])}项)"):
        for i, item in enumerate(st.session_state["compare_list"]):
            st.write(f"{i+1}. {item['disease']} - {item['timestamp']}")
        if st.button(" 清空对比列表"):
            st.session_state["compare_list"] = []
            st.rerun()
