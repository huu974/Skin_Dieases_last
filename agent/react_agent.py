"""
皮肤病诊断智能体
"""
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import yolo_detect, skin_classify, rag_query
import os
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("SkinAgent")


class SkinDiagnosisAgent:
    def __init__(self):
        self.chat_history = []
        self.system_prompt = load_system_prompts()
        self.image_analysis_done = False
        self.asked_symptoms = False
        self.cached_analysis = None
        self.pending_image_path = None


    """设置图片路径"""
    def set_image(self, image_path: str):
        self.pending_image_path = image_path


    """只运行一次检测和分类，结果缓存"""
    def analyze_image_once(self, image_path: str):
        if self.image_analysis_done:
            return self.cached_analysis
        
        logger.info(f"[YOLO] 开始检测皮损区域: {image_path}")
        yolo_result = yolo_detect.invoke({"image_path": image_path})
        logger.info(f"[YOLO] 检测完成: {yolo_result}")
        
        logger.info("[分类模型] 开始疾病分类")
        classify_result = skin_classify.invoke({"image_path": image_path})
        logger.info(f"[分类模型] 分类完成: {classify_result}")
        
        self.cached_analysis = {
            "yolo": yolo_result,
            "classify": classify_result
        }
        self.image_analysis_done = True
        return self.cached_analysis


    """支持图像分析的多轮对话"""
    def chat(self, query: str):
        # 第一次对话且有图片：自动检测 + 询问症状
        if self.pending_image_path and not self.asked_symptoms:
            logger.info("开始图像分析流程")
            result = self.analyze_image_once(self.pending_image_path)
            logger.info("图像分析完成，开始生成回复")
            
            first_prompt = f"""已对您的皮肤图像完成分析：
- 检测结果：{result['yolo']}
- 疾病分类：{result['classify']}

请根据以上结果，主动询问用户以下症状信息：
1. 这个部位有没有瘙痒、疼痛等不适感？
2. 出现多长时间了？
3. 有没有明显变化（变大、颜色加深等）？

询问时要简洁，然后根据用户回答结合知识库给出建议。"""
            
            messages = [SystemMessage(content=self.system_prompt)]
            messages.append(HumanMessage(content=first_prompt))
            
            response = chat_model.invoke(messages)
            ai_response = response.content
            
            self.chat_history.append(HumanMessage(content=first_prompt))
            self.chat_history.append(AIMessage(content=ai_response))
            self.asked_symptoms = True
            
            return ai_response
        messages = [SystemMessage(content=self.system_prompt)]
        messages.extend(self.chat_history)
        messages.append(HumanMessage(content=query))

        response = chat_model.invoke(messages)
        ai_response = response.content

        self.chat_history.append(HumanMessage(content=query))
        self.chat_history.append(AIMessage(content=ai_response))

        return ai_response


    """流式版本"""
    def execute_stream(self, query: str):
        result = self.chat(query)
        yield result


    """清空对话历史"""
    def clear_history(self):
        self.chat_history = []
        self.asked_symptoms = False


    """保存对话历史"""
    def save_history(self, filepath: str = "conversation_history.json"):
        import json
        history = []
        for msg in self.chat_history:
            msg_type = "human" if isinstance(msg, HumanMessage) else "ai"
            history.append({"type": msg_type, "content": msg.content})
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return len(history)


    """加载对话历史"""
    def load_history(self, filepath: str = "conversation_history.json"):
        import json
        if not os.path.exists(filepath):
            return 0
        with open(filepath, 'r', encoding='utf-8') as f:
            history = json.load(f)
        for item in history:
            if item['type'] == 'human':
                self.chat_history.append(HumanMessage(content=item['content']))
            else:
                self.chat_history.append(AIMessage(content=item['content']))
        return len(history)
