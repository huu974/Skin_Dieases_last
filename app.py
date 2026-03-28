"""
简单的streamlit
"""

import time
import tempfile
import streamlit as st
from agent.react_agent import SkinDiagnosisAgent

st.title("皮肤病诊断助手")
st.divider()

uploaded_file = st.file_uploader("上传皮肤图像（可选）", type=["jpg", "jpeg", "png"])

if "agent" not in st.session_state:
    st.session_state["agent"] = SkinDiagnosisAgent()

if uploaded_file:
    st.image(uploaded_file, caption="已上传图像")
    if "pending_image" not in st.session_state:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_file.getvalue())
            st.session_state["pending_image"] = tmp.name

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("请描述您的皮肤问题...")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    agent = st.session_state["agent"]

    if "pending_image" in st.session_state:
        agent.pending_image_path = st.session_state["pending_image"]

    with st.spinner("智能客服思考中..."):
        response = agent.chat(prompt)

        st.chat_message("assistant").write(response)
        st.session_state["message"].append({"role": "assistant", "content": response})

        if "pending_image" in st.session_state:
            del st.session_state["pending_image"]

        st.rerun()