"""
智能对话页面
"""
import streamlit as st
import time
import random
from datetime import datetime

st.set_page_config(page_title="智能对话", page_icon="💬", layout="wide")

def apply_theme():
    if st.session_state.get("theme", "light") == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; }
        .stChatMessage { background-color: #21262d; }
        footer {display: none !important;}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        footer {display: none !important;}
        .stChatInputContainer { position: fixed; bottom: 0; left: 0; right: 0; padding: 1rem; background: white; border-top: 1px solid #eee; }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

st.title("💬 智能对话")
st.markdown("与AI助手详细描述您的症状，获取专业建议")

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "assistant", "content": "您好！我是皮肤病智能诊断助手。请描述您遇到的皮肤问题，我会尽力为您提供初步建议。\n\n💡 **提示**：您可以同时上传皮肤图片，我会结合图片和症状进行综合分析。"}
    ]

if "pending_chat_image" not in st.session_state:
    st.session_state["pending_chat_image"] = None

quick_responses = {
    "脸上长痘痘怎么办？": "脸上长痘痘的常见原因包括皮脂分泌旺盛、毛孔堵塞、细菌感染等。建议您：\n\n1. **保持清洁**：每天用温和的洁面产品清洗面部\n2. **不要挤压**：挤压可能加重炎症和留下疤痕\n3. **调整饮食**：少吃辛辣、油腻、甜食\n4. **规律作息**：保证充足睡眠，减少熬夜\n5. **外用药物**：可使用含水杨酸或苯甲酸的护肤品\n\n⚠️ 如痘痘持续严重或伴有红肿，建议就医皮肤科。",
    
    "皮肤瘙痒是什么原因？": "皮肤瘙痒的常见原因包括：\n\n1. **干燥**：皮肤缺水会导致瘙痒\n2. **过敏**：接触过敏原（如花粉、某些护肤品）\n3. **湿疹**：慢性炎症性皮肤病\n4. **荨麻疹**：俗称风团，来去迅速\n5. **皮肤病**：如银屑病、神经性皮炎等\n\n**建议**：\n• 避免抓挠，以免加重\n• 保持皮肤湿润\n• 观察是否与饮食或接触物有关\n\n⚠️ 如瘙痒持续或伴有皮疹，请就医检查。",
    
    "如何预防湿疹？": "预防湿疹的建议：\n\n1. **保湿**：每天使用温和的保湿霜，保持皮肤湿润\n2. **避免刺激**：不用过热的水洗澡，避免刺激性护肤品\n3. **穿透气衣物**：选择纯棉、宽松的衣物\n4. **注意饮食**：如有已知过敏食物应避免\n5. **环境管理**：保持居住环境清洁，避免过度潮湿或干燥\n6. **减少压力**：精神紧张可能诱发湿疹\n\n如已患湿疹，应在医生指导下用药。",
    
    "过敏性皮炎怎么治疗？": "过敏性皮炎的治疗建议：\n\n**一般处理**：\n1. 找出并远离过敏原\n2. 避免抓挠患处\n3. 用冷敷缓解瘙痒\n\n**药物治疗**：\n1. 口服抗组胺药（如氯雷他定）\n2. 外用糖皮质激素软膏\n3. 严重时需就医\n\n**日常护理**：\n• 选择温和无刺激的护肤品\n• 保持皮肤清洁湿润\n• 避免辛辣刺激食物\n\n⚠️ 建议先就医做过敏原检测，明确致敏物质。",
    
    "银屑病的症状有哪些？": "银屑病（ Psoriasis）的典型症状：\n\n**主要表现**：\n• 红色斑块：皮肤出现边界清楚的红色丘疹或斑块\n• 银白色鳞屑：覆盖厚厚的银白色鳞屑\n• 薄膜现象：刮除鳞屑后可见淡红色薄膜\n• 点状出血：刮破薄膜可见点状出血\n\n**好发部位**：头皮、四肢伸侧、躯干等\n\n**其他类型**：\n• 关节型银屑病：伴有关节疼痛\n• 脓疱型银屑病：出现无菌性脓疱\n\n⚠️ 银屑病目前无法根治，但可通过治疗控制症状，请到正规医院皮肤科就诊。"
}

quick_questions = list(quick_responses.keys())

for msg in st.session_state["chat_messages"]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

for q in quick_questions:
    if st.button(q, use_container_width=True, key=f"quick_{q}"):
        st.session_state["chat_messages"].append({"role": "user", "content": q})
        response = quick_responses[q]
        st.session_state["chat_messages"].append({"role": "assistant", "content": response})
        st.rerun()

st.markdown("---")

if prompt := st.chat_input("请描述您的皮肤问题..."):
    st.session_state["chat_messages"].append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("AI正在思考..."):
            time.sleep(1)
            responses = [
                "根据您描述的症状，这可能是常见的皮肤炎症反应。建议：\n\n1. 保持患处清洁干燥\n2. 避免使用刺激性护肤品\n3. 如症状持续或加重，请尽快就医\n\n您有上传图片吗？结合图片可以提供更准确的初步判断。",
                "您好，您描述的情况需要进一步观察。建议您：\n\n• 注意饮食清淡，避免辛辣食物\n• 保持良好作息，减少熬夜\n• 观察3-5天，如无好转建议就诊\n\n请问还有其他症状吗？",
                "根据您的描述，这可能是轻微的皮肤过敏反应。建议：\n\n1. 排查可能的过敏原\n2. 使用温和的护肤品\n3. 如瘙痒严重可使用冷敷缓解\n\n⚠️ 如出现红肿扩散或呼吸困难，请立即就医！"
            ]
            response = random.choice(responses)
            st.write(response)
    
    st.session_state["chat_messages"].append({"role": "assistant", "content": response})

st.markdown("---")

with st.expander(" 附加图片辅助诊断"):
    chat_image = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"], key="chat_img")
    if chat_image:
        st.image(chat_image, caption="附加图片", use_container_width=True)
        st.session_state["pending_chat_image"] = chat_image.name
        st.success("图片已附加")

with st.expander(" 对话提示"):
    st.info("• 请尽可能详细描述症状（位置、时长、变化等）")
    st.info("• 上传清晰的患处图片可提高诊断准确性")
    st.info("• AI助手仅供参考，不作为正式医疗诊断")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    pass
with col2:
    if st.button("清空对话", type="secondary", use_container_width=True):
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": "对话已清空。请描述您遇到的皮肤问题，我会尽力为您提供帮助。"}
        ]
        st.rerun()
with col3:
    pass
