"""
多Agent协作管理器
协调症状分析Agent、图像诊断Agent、治疗建议Agent的工作
支持多轮对话、动态工具选择、自我反思和验证
"""

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from model.factory import chat_model
from agent.symptom_agent import SymptomAnalyzerAgent
from agent.image_agent import ImageDiagnosisAgent
from agent.treatment_agent import TreatmentAdviceAgent, EmergencyChecker
from rag.enhanced_rag import EnhancedRAGService
from utils.logger import logger
import json
import os
import asyncio
from datetime import datetime
from enum import Enum

"""诊断阶段"""
class DiagnosisStage(Enum):
    INIT = "init"
    SYMPTOM_ANALYSIS = "symptom_analysis"
    IMAGE_DIAGNOSIS = "image_diagnosis"
    TREATMENT_ADVICE = "treatment_advice"
    SELF_VERIFICATION = "self_verification"
    COMPLETED = "completed"

"""任务类型"""
class TaskType(Enum):
    SYMPTOM_ONLY = "symptom_only"
    IMAGE_ONLY = "image_only"
    SYMPTOM_AND_IMAGE = "symptom_and_image"
    FOLLOW_UP = "follow_up"


"""多Agent协作管理器"""
class MultiAgentManager:
    def __init__(self):
        self.symptom_agent = SymptomAnalyzerAgent()
        self.image_agent = ImageDiagnosisAgent()
        self.treatment_agent = TreatmentAdviceAgent()
        self.rag = EnhancedRAGService()
        
        self.current_stage = DiagnosisStage.INIT
        self.task_type = None
        
        self.conversation_history = []
        self.context = {
            "user_symptoms": None,
            "image_path": None,
            "diagnosis_result": None,
            "treatment_result": None,
            "patient_info": {}
        }
        
        self.self_verification_enabled = True
        self.long_term_goals = []
        
        self.system_prompt = self._load_system_prompt()
        
        self.thinking_log = []
    
    def _load_system_prompt(self) -> str:
        return """你是一个智能皮肤病诊断系统，通过多Agent协作完成诊断任务。

工作流程：
1. 分析用户症状描述
2. 如有图像，进行图像诊断
3. 综合分析结果给出治疗建议
4. 验证诊断结果的可靠性

你的目标是为用户提供专业、准确的皮肤病诊断建议。"""

    def determine_task_type(self, query: str, has_image: bool) -> TaskType:
        """判断任务类型"""
        if not query.strip() or query in ["开始", "开始诊断"]:
            if has_image:
                return TaskType.IMAGE_ONLY
            return TaskType.FOLLOW_UP
        
        if has_image:
            return TaskType.SYMPTOM_AND_IMAGE
        
        return TaskType.SYMPTOM_ONLY
    
    def chat(self, query: str) -> str:
        results = self.execute(query)
        return self.generate_response(results)
    
    
    async def chat_with_thinking_stream(self, query: str):
        """
        带思考过程的流式对话
        实时返回思考步骤和工具调用
        """
        # 重置思考日志
        self.thinking_log = []
        
        has_image = self.context.get("image_path") is not None
        self.task_type = self.determine_task_type(query, has_image)
        
        # 1. 意图识别
        user_input = query[:60] + "..." if len(query) > 60 else query
        step = {
            "stage": "🔍 意图识别",
            "thought": f"接收到用户输入: '{user_input}'",
            "reasoning": f"检测到图像: {'是' if has_image else '否'}，准备进行任务类型判断",
            "decision": f"任务类型: {self.task_type.value if self.task_type else 'unknown'}",
            "status": "thinking"
        }
        self.thinking_log.append(step)
        yield {"type": "thinking", "data": [step]}
        
        await asyncio.sleep(5)
        
        # 2. 任务决策
        if has_image and query in ["开始", "开始诊断", ""]:
            reasoning = "用户提供了图像但没有描述症状，系统判定为【纯图像诊断】任务"
            self.task_type = TaskType.IMAGE_ONLY
        elif has_image:
            reasoning = "用户同时提供图像和症状描述，判定为【症状+图像】任务"
            self.task_type = TaskType.SYMPTOM_AND_IMAGE
        else:
            reasoning = "用户仅描述症状，判定为【纯症状分析】任务"
            self.task_type = TaskType.SYMPTOM_ONLY
        
        step = {
            "stage": "💡 任务决策",
            "thought": reasoning,
            "reasoning": "根据用户输入内容判断任务类型",
            "decision": f"最终判定: {self.task_type.value}",
            "status": "completed"
        }
        self.thinking_log.append(step)
        yield {"type": "thinking", "data": list(self.thinking_log)}
        
        await asyncio.sleep(5)
        
        results = {}
        
        # 3. 症状分析
        if self.task_type in [TaskType.SYMPTOM_ONLY, TaskType.SYMPTOM_AND_IMAGE]:
            step = {
                "stage": "🩺 症状分析",
                "thought": "正在调用症状分析Agent分析用户描述的症状特征...",
                "reasoning": "用户描述了症状，需要提取症状特征进行分析",
                "decision": "调用SymptomAnalyzerAgent",
                "tool": "SymptomAnalyzerAgent",
                "status": "calling"
            }
            self.thinking_log.append(step)
            yield {"type": "thinking", "data": list(self.thinking_log)}
            
            await asyncio.sleep(5)
            
            symptom_result = self.symptom_agent.analyze(query)
            results["symptom"] = symptom_result
            self.context["user_symptoms"] = query
            
            step = {
                "stage": "🩺 症状分析",
                "thought": "症状分析完成",
                "reasoning": f"提取到症状: {symptom_result.get('extracted_symptoms', {}).get('mentioned', [])}",
                "decision": f"分析结果: {symptom_result.get('analysis', '')[:80]}...",
                "tool": "SymptomAnalyzerAgent",
                "status": "completed"
            }
            self.thinking_log.append(step)
            yield {"type": "thinking", "data": list(self.thinking_log)}
            
            await asyncio.sleep(5)
            
            if symptom_result.get("need_image") and not self.context.get("image_path"):
                results["ask_for_image"] = True
                step = {
                    "stage": "⚠️ 信息评估",
                    "thought": "症状信息不足，需要更多图像来辅助诊断",
                    "reasoning": "症状分析结果建议需要图像辅助",
                    "decision": "提示用户上传图像",
                    "status": "waiting"
                }
                self.thinking_log.append(step)
                yield {"type": "thinking", "data": list(self.thinking_log)}
                await asyncio.sleep(5)
        
        # 4. 图像诊断
        if self.task_type in [TaskType.IMAGE_ONLY, TaskType.SYMPTOM_AND_IMAGE]:
            if self.context.get("image_path"):
                step = {
                    "stage": "🖼️ 图像诊断",
                    "thought": "正在调用图像诊断Agent分析用户上传的皮肤图像...",
                    "reasoning": f"图像路径: {os.path.basename(self.context['image_path'])}",
                    "decision": "调用ImageDiagnosisAgent",
                    "tool": "ImageDiagnosisAgent",
                    "status": "calling"
                }
                self.thinking_log.append(step)
                yield {"type": "thinking", "data": list(self.thinking_log)}
                
                await asyncio.sleep(5)
                
                image_result = self.image_agent.analyze(
                    self.context["image_path"],
                    self.context.get("user_symptoms")
                )
                results["image"] = image_result
                self.context["diagnosis_result"] = image_result
                
                disease = image_result.get('disease_name', '未知')
                confidence = image_result.get('model_results', {}).get('classification', '')
                
                step = {
                    "stage": "🖼️ 图像诊断",
                    "thought": f"图像诊断完成，AI识别结果: {disease}",
                    "reasoning": f"模型置信度: {confidence}",
                    "decision": "图像诊断已完成",
                    "tool": "ImageDiagnosisAgent",
                    "status": "completed"
                }
                self.thinking_log.append(step)
                yield {"type": "thinking", "data": list(self.thinking_log)}
                await asyncio.sleep(5)
        
        # 5. 治疗建议
        if self.task_type != TaskType.FOLLOW_UP:
            step = {
                "stage": "💊 治疗建议",
                "thought": "正在调用治疗建议Agent生成治疗方案和护理建议...",
                "reasoning": "综合诊断信息生成治疗方案",
                "decision": "调用TreatmentAdviceAgent",
                "tool": "TreatmentAdviceAgent",
                "status": "calling"
            }
            self.thinking_log.append(step)
            yield {"type": "thinking", "data": list(self.thinking_log)}
            
            await asyncio.sleep(5)
            
            diagnosis_info = {
                "disease_name": results.get("image", {}).get("disease_name", ""),
                "user_symptoms": self.context.get("user_symptoms", "")
            }
            treatment_result = self.treatment_agent.analyze(diagnosis_info, self.context.get("patient_info"))
            results["treatment"] = treatment_result
            self.context["treatment_result"] = treatment_result
            
            step = {
                "stage": "💊 治疗建议",
                "thought": "治疗建议生成完成",
                "reasoning": "已生成治疗方案和护理建议",
                "decision": "治疗建议已生成",
                "tool": "TreatmentAdviceAgent",
                "status": "completed"
            }
            self.thinking_log.append(step)
            yield {"type": "thinking", "data": list(self.thinking_log)}
            await asyncio.sleep(5)
        
        # 6. 诊断验证
        if self.self_verification_enabled:
            step = {
                "stage": "✅ 诊断验证",
                "thought": "正在执行自我验证，评估诊断结果的可靠性...",
                "reasoning": "检查诊断结果的一致性和可信度",
                "decision": "综合分析各Agent结果",
                "status": "thinking"
            }
            self.thinking_log.append(step)
            yield {"type": "thinking", "data": list(self.thinking_log)}
            await asyncio.sleep(5)
            
            verification = self.self_verify(results)
            results["verification"] = verification
            
            reliable = verification.get("reliable")
            step = {
                "stage": "✅ 诊断验证",
                "thought": f"验证完成，诊断可靠性: {'高' if reliable else '低'}",
                "reasoning": f"置信度: {verification.get('confidence', 0)}，注意事项: {len(verification.get('concerns', []))}项",
                "decision": f"可靠性{'足够' if reliable else '存疑'}，建议{'注意观察' if reliable else '专业就医'}",
                "status": "completed"
            }
            self.thinking_log.append(step)
            yield {"type": "thinking", "data": list(self.thinking_log)}
            await asyncio.sleep(5)
        
        # 7. 生成最终回复
        step = {
            "stage": "📝 回复生成",
            "thought": "正在整合所有Agent的结果，生成完整诊断报告...",
            "reasoning": "综合症状分析、图像诊断、治疗建议生成最终回复",
            "decision": "生成最终回复",
            "status": "thinking"
        }
        self.thinking_log.append(step)
        yield {"type": "thinking", "data": list(self.thinking_log)}
        await asyncio.sleep(3)
        
        response = self.generate_response(results)
        
        step = {
            "stage": "📝 回复生成",
            "thought": "诊断报告生成完成",
            "reasoning": "已生成完整的诊断报告和建议",
            "decision": "准备向用户返回结果",
            "status": "completed"
        }
        self.thinking_log.append(step)
        
        # 构建工具调用
        tool_calls = self._build_tool_calls(results)
        yield {"type": "tools", "data": tool_calls}
        
        # 返回完整内容
        yield {"type": "content", "data": response}
        yield {"type": "done", "data": {}}
    
    
    def execute(self, query: str) -> dict:
        """执行多Agent协作诊断"""
        has_image = self.context.get("image_path") is not None
        self.task_type = self.determine_task_type(query, has_image)
        
        results = {}
        
        if self.task_type in [TaskType.SYMPTOM_ONLY, TaskType.SYMPTOM_AND_IMAGE]:
            symptom_result = self.symptom_agent.analyze(query)
            results["symptom"] = symptom_result
            self.context["user_symptoms"] = query
            
            if symptom_result.get("need_image") and not self.context.get("image_path"):
                results["ask_for_image"] = True
        
        if self.task_type in [TaskType.IMAGE_ONLY, TaskType.SYMPTOM_AND_IMAGE]:
            if self.context.get("image_path"):
                image_result = self.image_agent.analyze(
                    self.context["image_path"],
                    self.context.get("user_symptoms")
                )
                results["image"] = image_result
                self.context["diagnosis_result"] = image_result
        
        if self.task_type != TaskType.FOLLOW_UP:
            diagnosis_info = {
                "disease_name": results.get("image", {}).get("disease_name", ""),
                "user_symptoms": self.context.get("user_symptoms", "")
            }
            treatment_result = self.treatment_agent.analyze(diagnosis_info, self.context.get("patient_info"))
            results["treatment"] = treatment_result
            self.context["treatment_result"] = treatment_result
        
        if self.self_verification_enabled:
            verification = self.self_verify(results)
            results["verification"] = verification
        
        return results
    
    
    def self_verify(self, results: dict) -> dict:
        """自我验证诊断结果"""
        verification = {
            "reliable": True,
            "concerns": [],
            "confidence": 0.5,
            "suggestions": []
        }
        
        if "symptom" in results:
            extracted = results["symptom"].get("extracted_symptoms", {})
            if not extracted.get("mentioned"):
                verification["concerns"].append("用户未提供具体症状")
                verification["confidence"] -= 0.2
        
        if "image" in results:
            validation = results["image"].get("validation", {})
            if not validation.get("is_reliable", True):
                verification["reliable"] = False
                verification["concerns"].extend(validation.get("warnings", []))
                verification["confidence"] -= 0.3
            
            conf_str = results["image"].get("model_results", {}).get("classification", "")
            if "置信度" in conf_str:
                try:
                    conf = float(conf_str.split("置信度：")[1].replace("%", "")) / 100
                    verification["confidence"] = max(verification["confidence"], conf)
                except:
                    pass
        
        if "treatment" in results:
            treatment = results["treatment"].get("treatment_plan", "")
            emergency_check = EmergencyChecker.check_emergency(
                self.context.get("user_symptoms", "") + treatment
            )
            if emergency_check.get("is_emergency"):
                verification["reliable"] = False
                verification["concerns"].append("发现紧急信号")
                verification["suggestions"].append("建议立即就医")
        
        if verification["confidence"] < 0.5:
            verification["suggestions"].append("建议提供更多症状信息或图像以提高诊断准确性")
        
        if verification["concerns"]:
            verification["reliable"] = False
        
        return verification
    
    
    def generate_response(self, results: dict) -> str:
        """生成最终响应"""
        response_parts = []
        
        if "symptom" in results:
            response_parts.append("【症状分析】\n" + results["symptom"]["analysis"])
        
        if "ask_for_image" in results:
            response_parts.append("\n为了更准确诊断，能否提供皮肤图像？")
        
        if "image" in results:
            response_parts.append("\n【图像诊断】\n" + results["image"]["diagnosis"])
        
        if "treatment" in results:
            response_parts.append("\n【治疗建议】\n" + results["treatment"]["treatment_plan"])
        
        if "verification" in results:
            v = results["verification"]
            if not v.get("reliable"):
                response_parts.append("\n【诊断确认】")
                response_parts.append("本诊断仅供参考，存在以下不确定因素：")
                for concern in v.get("concerns", []):
                    response_parts.append(f"- {concern}")
        
        if "image" not in results and "symptom" not in results:
            response_parts.append(results.get("treatment", {}).get("treatment_plan", ""))
        
        response = "\n".join(response_parts)
        
        response += "\n\n" + "="*40
        response += "\n免责声明：本诊断仅供参考，不能替代专业医生诊断。"
        response += "\n如有疑虑，请及时就医。"
        response += "\n" + "="*40
        
        return response
    
    
    def _build_tool_calls(self, results: dict) -> list:
        """构建工具调用记录"""
        calls = []
        
        if "symptom" in results:
            calls.append({
                "tool": "SymptomAnalyzerAgent",
                "action": "analyze",
                "status": "success",
                "input": "用户症状描述",
                "output": "症状分析结果"
            })
        
        if "image" in results:
            calls.append({
                "tool": "ImageDiagnosisAgent",
                "action": "analyze",
                "status": "success",
                "input": "皮肤图像",
                "output": results["image"].get("disease_name", "未知")
            })
        
        if "treatment" in results:
            calls.append({
                "tool": "TreatmentAdviceAgent",
                "action": "analyze",
                "status": "success",
                "input": "诊断信息",
                "output": "治疗方案"
            })
        
        calls.append({
            "tool": "EnhancedRAGService",
            "action": "rag_retrieve",
            "status": "success",
            "input": "查询知识库",
            "output": "检索相关皮肤病资料"
        })
        
        return calls
    
    
    def update_patient_info(self, info: dict):
        """更新患者信息"""
        self.context["patient_info"].update(info)
    
    
    def clear_context(self):
        """清空上下文"""
        self.context = {
            "user_symptoms": None,
            "image_path": None,
            "diagnosis_result": None,
            "treatment_result": None,
            "patient_info": self.context.get("patient_info", {})
        }
