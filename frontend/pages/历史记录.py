"""
诊断历史记录
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="诊断历史", page_icon="", layout="wide")

def apply_theme():
    if st.session_state.get("theme", "light") == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

st.title(" 诊断历史")
st.markdown("查看和管理您的历史诊断记录")

if "diagnosis_results" not in st.session_state:
    st.session_state["diagnosis_results"] = []

if st.session_state["diagnosis_results"]:
    st.session_state["history_records"] = st.session_state["diagnosis_results"]
else:
    if "history_records" not in st.session_state:
        st.session_state["history_records"] = []

records = st.session_state["history_records"]

col1, col2 = st.columns(2)
with col1:
    st.metric("总诊断数", len(records))
with col2:
    if records:
        dates = [r.get("timestamp", "") for r in records if r.get("timestamp")]
        last_date = dates[0] if dates else "暂无"
        st.metric("最近诊断", last_date)
    else:
        st.metric("最近诊断", "暂无")

st.markdown("---")

if records:
    col_left, col_right = st.columns([4, 1])
    
    with col_left:
        disease_filter = st.selectbox(
            "按疾病筛选",
            ["全部"] + list(set([r.get("disease", "未知").split(" (")[0] for r in records]))
        )
    
    with col_right:
        sort_by = st.selectbox(
            "排序方式",
            ["最新优先", "置信度最高"]
        )
    
    filtered_records = records.copy()
    
    if disease_filter != "全部":
        filtered_records = [r for r in filtered_records if disease_filter in r.get("disease", "")]
    
    if sort_by == "置信度最高":
        filtered_records = sorted(filtered_records, key=lambda x: x.get("confidence", 0), reverse=True)
    
    st.markdown(f"**共 {len(filtered_records)} 条记录**")
    
    for i, record in enumerate(filtered_records):
        with st.container():
            severity = record.get("severity", "中等")
            severity_color = {"轻度": "", "中等": "", "重度": ""}.get(severity, "⚪")
            
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #333;">🦠 {record.get('disease', '未知疾病')}</h4>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 13px;">
                             {record.get('timestamp', '未知时间')} | 
                            {severity_color} {severity} | 
                            置信度: {record.get('confidence', 0)}%
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_del, _ = st.columns([1, 4])
            with col_del:
                if st.button(" 删除", key=f"del_history_{i}"):
                    st.session_state["history_records"] = [
                        r for r in st.session_state["history_records"] 
                        if r.get("image_name") != record.get("image_name") or not record.get("image_name")
                    ]
                    st.rerun()
else:
    st.info(" 暂无诊断记录，请先进行诊断分析")

st.markdown("---")

if st.button(" 导出历史记录", type="primary", use_container_width=True):
    if records:
        csv_data = "时间,疾病,置信度,严重程度\n"
        for r in records:
            csv_data += f"{r.get('timestamp', '')},{r.get('disease', '')},{r.get('confidence', 0)}%,{r.get('severity', '')}\n"
        
        st.download_button(
            label="下载 CSV",
            data=csv_data,
            file_name=f"诊断历史_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("暂无记录可导出")

if records:
    st.markdown("###  诊断趋势")
    
    df_records = pd.DataFrame(records)
    if "timestamp" in df_records.columns and len(df_records) > 0:
        df_records["date"] = pd.to_datetime(df_records["timestamp"], format="%Y-%m-%d %H:%M", errors="coerce")
        df_records = df_records.dropna(subset=["date"])
        
        if not df_records.empty:
            df_records["date_only"] = df_records["date"].dt.date
            daily_counts = df_records.groupby("date_only").size().reset_index(name="诊断数")
            daily_counts.columns = ["日期", "诊断数"]
            
            if not daily_counts.empty:
                st.line_chart(daily_counts.set_index("日期"))
            else:
                st.info("数据不足以生成趋势图")
        else:
            st.info("无法解析日期数据")
    else:
        st.info("暂无趋势数据")
