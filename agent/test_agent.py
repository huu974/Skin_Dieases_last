"""
Agent 与 RAG 功能测试脚本
"""
import sys
import os

# 获取项目根目录（上级目录）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def test_rag():
    """测试 RAG 检索"""
    print("=" * 50)
    print("测试 RAG 检索")
    print("=" * 50)
    
    from rag.enhanced_rag import EnhancedRAGService
    
    rag = EnhancedRAGService()
    query = "湿疹怎么治疗"
    
    print(f"\n查询: {query}")
    result = rag.rag_retrieve(query)
    
    print(f"\n检索到 {len(result['documents'])} 个文档")
    print(f"\n回答:\n{result['answer'][:300]}...")
    print("\n" + "-" * 50)


def test_symptom_agent():
    """测试症状分析 Agent"""
    print("=" * 50)
    print("测试症状分析 Agent")
    print("=" * 50)
    
    from agent.symptom_agent import SymptomAnalyzerAgent
    
    agent = SymptomAnalyzerAgent()
    query = "脸上长了很多红疙瘩，很痒，一周了"
    
    print(f"\n用户描述: {query}")
    result = agent.analyze(query)
    
    print(f"\n提取的症状: {result['extracted_symptoms']}")
    print(f"\n分析结果:\n{result['analysis'][:300]}...")
    print("\n" + "-" * 50)


def test_image_agent():
    """测试图像诊断 Agent"""
    print("=" * 50)
    print("测试图像诊断 Agent")
    print("=" * 50)
    
    from agent.image_agent import ImageDiagnosisAgent
    
    agent = ImageDiagnosisAgent()
    image_path = input("请输入图像路径（或直接回车跳过）: ").strip()
    
    if image_path:
        result = agent.analyze(image_path, "脸上有红斑")
        print(f"\n诊断结果:\n{result['diagnosis'][:300]}...")
    else:
        print("跳过图像测试")
    print("\n" + "-" * 50)


def test_treatment_agent():
    """测试治疗建议 Agent"""
    print("=" * 50)
    print("测试治疗建议 Agent")
    print("=" * 50)
    
    from agent.treatment_agent import TreatmentAdviceAgent
    
    agent = TreatmentAdviceAgent()
    diagnosis_info = {
        "disease_name": "湿疹",
        "user_symptoms": "脸上长红疙瘩，很痒，一周了"
    }
    
    print(f"\n诊断信息: {diagnosis_info}")
    result = agent.analyze(diagnosis_info)
    
    print(f"\n治疗建议:\n{result['treatment_plan'][:300]}...")
    print("\n" + "-" * 50)


def test_multi_agent():
    """测试多 Agent 协作"""
    print("=" * 50)
    print("测试多 Agent 协作")
    print("=" * 50)
    
    from agent.multi_agent_manager import MultiAgentManager
    
    agent = MultiAgentManager()
    query = "脸上长了很多红疙瘩，很痒，一周了"
    
    print(f"\n用户问题: {query}")
    
    result = agent.execute(query)
    response = agent.generate_response(result)
    
    print(f"\n最终回复:\n{response}")
    print("\n" + "-" * 50)


def main():
    print("\n" + "=" * 50)
    print("  皮肤疾病诊断系统 - 功能测试")
    print("=" * 50 + "\n")
    
    print("1. 测试 RAG 检索")
    print("2. 测试症状分析 Agent")
    print("3. 测试图像诊断 Agent")
    print("4. 测试治疗建议 Agent")
    print("5. 测试多 Agent 协作（完整流程）")
    print("6. 运行全部测试")
    print("0. 退出")
    
    choice = input("\n请选择 (0-6): ").strip()
    
    if choice == "1":
        test_rag()
    elif choice == "2":
        test_symptom_agent()
    elif choice == "3":
        test_image_agent()
    elif choice == "4":
        test_treatment_agent()
    elif choice == "5":
        test_multi_agent()
    elif choice == "6":
        test_rag()
        test_symptom_agent()
        test_treatment_agent()
        test_multi_agent()
    else:
        print("退出")


if __name__ == "__main__":
    main()
