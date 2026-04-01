"""
LLM对话服务 - RAG + Agent
"""
import time
import asyncio
from typing import List, Dict, Optional


class LLMChatService:
    """LLM对话服务"""
    
    MEDICAL_TERMS = {
        "银屑病": "一种慢性炎症性皮肤病，表现为红斑、鳞屑",
        "湿疹": "皮肤炎症反应，伴随瘙痒和红斑",
        "痤疮": "毛囊皮脂腺单位的慢性炎症性疾病",
        "荨麻疹": "皮肤黏膜小血管扩张及渗透性增加导致的局限性水肿",
    }
    
    def __init__(self):
        self.initialized = False
    
    async def initialize(self):
        """初始化LLM服务"""
        if not self.initialized:
            # TODO: 初始化LLM和RAG
            # from rag.retriever import SkinDiseaseRetriever
            # from agent.react_agent import SkinDiagnosisAgent
            self.initialized = True
    
    async def chat(
        self, 
        message: str, 
        context: Optional[Dict] = None,
        images: Optional[List[str]] = None
    ) -> Dict:
        """
        智能对话
        - RAG检索相关知识
        - Agent推理
        - 风险评估
        """
        start_time = time.time()
        
        await self.initialize()
        
        # TODO: 实际调用RAG+Agent
        # retriever = SkinDiseaseRetriever()
        # agent = SkinDiagnosisAgent()
        # context_docs = await retriever.retrieve(message)
        # response, steps = await agent.chat(message, context_docs)
        
        # 模拟响应
        response = self._generate_response(message)
        steps = [
            {"step": "理解问题", "content": "分析用户描述的皮肤症状"},
            {"step": "知识检索", "content": "从知识库中检索相关疾病信息"},
            {"step": "症状匹配", "content": "将症状与已知疾病进行匹配"},
            {"step": "建议生成", "content": "生成护理建议和就医指导"}
        ]
        
        # 术语标注
        annotations = self._extract_medical_terms(message)
        
        # 风险评估
        risk_assessment = self._assess_risk(message)
        
        # 转诊建议
        referral = self._generate_referral_suggestion(message, risk_assessment)
        
        processing_time = int(time.time() - start_time)
        
        return {
            "reply": response,
            "annotations": annotations,
            "reasoning_steps": steps,
            "risk_assessment": risk_assessment,
            "referral_suggestion": referral,
            "processing_time": processing_time
        }
    
    def _generate_response(self, message: str) -> str:
        """生成回复"""
        if any(keyword in message for keyword in ["痒", "瘙痒", "红"]):
            return (
                "根据您描述的症状，可能是湿疹或荨麻疹。\n\n"
                "建议：\n"
                "1. 保持皮肤清洁干燥\n"
                "2. 避免抓挠，以免继发感染\n"
                "3. 使用温和的保湿霜\n"
                "4. 如症状持续或加重，建议就医\n\n"
                "⚠️ 本回答仅供参考，不能替代专业医疗诊断"
            )
        elif any(keyword in message for keyword in ["痘痘", "痤疮", "粉刺"]):
            return (
                "根据您描述的症状，可能是痤疮。\n\n"
                "建议：\n"
                "1. 保持面部清洁，每天用温和的洁面产品\n"
                "2. 不要挤压痘痘，以免留下疤痕\n"
                "3. 规律作息，减少熬夜\n"
                "4. 避免高糖高脂饮食\n"
                "5. 如症状严重，建议就医\n\n"
                "⚠️ 本回答仅供参考"
            )
        else:
            return (
                "感谢您的咨询。\n\n"
                "为了更好地帮助您，请提供更多症状信息，如：\n"
                "- 症状持续时间\n"
                "- 是否有瘙痒、疼痛\n"
                "- 症状部位\n"
                "- 是否有其他不适\n\n"
                "⚠️ 本回答仅供参考，建议如有疑虑及时就医"
            )
    
    def _extract_medical_terms(self, message: str) -> List[Dict]:
        """提取医疗术语"""
        annotations = []
        for term, definition in self.MEDICAL_TERMS.items():
            if term in message:
                annotations.append({
                    "term": term,
                    "definition": definition,
                    "category": "disease"
                })
        return annotations
    
    def _assess_risk(self, message: str) -> Dict:
        """风险评估"""
        high_risk_keywords = ["出血", "溃烂", "疼痛剧烈", "快速扩散"]
        medium_risk_keywords = ["反复", "长期", "加重"]
        
        if any(keyword in message for keyword in high_risk_keywords):
            return {
                "level": "high",
                "factors": ["症状描述显示较高风险"],
                "description": "建议尽快就医"
            }
        elif any(keyword in message for keyword in medium_risk_keywords):
            return {
                "level": "medium",
                "factors": ["症状持续时间较长"],
                "description": "建议近期就医"
            }
        else:
            return {
                "level": "low",
                "factors": ["症状相对轻微"],
                "description": "可先观察，如加重则就医"
            }
    
    def _generate_referral_suggestion(
        self, 
        message: str, 
        risk_assessment: Dict
    ) -> Dict:
        """转诊建议"""
        if risk_assessment["level"] == "high":
            return {
                "suggested": True,
                "reason": "症状显示较高风险",
                "urgency": "urgent",
                "nearby_clinics": None
            }
        return {
            "suggested": False,
            "reason": "症状相对轻微",
            "urgency": "normal",
            "nearby_clinics": None
        }
    
    async def get_quick_questions(self) -> List[Dict]:
        """获取快捷问题"""
        return [
            {"id": 1, "question": "如何预防湿疹？", "category": "prevention"},
            {"id": 2, "question": "痤疮需要注意什么饮食？", "category": "diet"},
            {"id": 3, "question": "银屑病会传染吗？", "category": "awareness"},
            {"id": 4, "question": "荨麻疹反复发作怎么办？", "category": "treatment"},
            {"id": 5, "question": "皮肤干燥如何护理？", "category": "care"},
            {"id": 6, "question": "如何判断黑痣是否恶性？", "category": "awareness"},
        ]


llm_chat_service = LLMChatService()
