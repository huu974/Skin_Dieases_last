"""
皮肤病诊断Agent启动入口 - 新版多Agent系统（详细日志版）
"""
import sys
import os
import logging

# 设置日志级别为DEBUG，可以看到更详细的信息
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

from agent.multi_agent_manager import MultiAgentManager
from utils.logger import logger

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HISTORY_FILE = "conversation_history.json"


def print_decision_flow(agent, query):
    """打印决策流程"""
    print("\n" + "="*60)
    print("🔍 智能体决策过程")
    print("="*60)
    
    # 1. 判断任务类型
    has_image = agent.context.get("image_path") is not None
    task_type = agent.determine_task_type(query, has_image)
    print(f"\n📌 步骤1: 任务类型判断")
    print(f"   - 用户输入: {query[:50]}...")
    print(f"   - 是否有图像: {has_image}")
    print(f"   - 任务类型: {task_type.value}")
    
    # 2. 执行流程
    print(f"\n📌 步骤2: 执行Agent流程")
    print(f"   - 当前阶段: {agent.current_stage.value}")
    
    # 3. 结果展示
    print(f"\n📌 步骤3: Agent执行结果")


def main():
    print("=" * 50)
    print("     皮肤疾病诊断助手 (多Agent版)")
    print("=" * 50)
    print("命令：")
    print("  'quit' / 'exit' - 退出程序")
    print("  'save' - 保存对话历史")
    print("  'clear' - 清空历史")
    print("  'debug' - 切换详细日志模式")
    print()
    
    print("正在初始化诊断系统...\n")
    agent = MultiAgentManager()
    
    print("-" * 50)
    image_path = input("请提供皮肤图像路径（直接回车跳过）：").strip()
    
    if image_path:
        if os.path.exists(image_path):
            agent.set_image(image_path)
            print(f"\n已加载图像: {os.path.basename(image_path)}\n")
        else:
            print(f"\n图像文件不存在，将以文字问答模式运行\n")
    
    print("-" * 50)
    print("AI: ", end="", flush=True)
    
    try:
        # 先打印决策流程
        print_decision_flow(agent, "开始诊断")
        
        for chunk in agent.execute_stream("开始诊断"):
            print(chunk, end="", flush=True)
    except Exception as e:
        logger.error(f"诊断过程出错: {e}")
        print(f"\n诊断过程出错: {e}")

    print()
    print("-" * 50)

    debug_mode = True
    
    while True:
        query = input("\n您: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        if query.lower() == 'debug':
            debug_mode = not debug_mode
            print(f"详细日志模式: {'开启' if debug_mode else '关闭'}\n")
            continue
        
        if query.lower() == 'save':
            print("请手动保存（功能开发中）")
            continue
        
        if query.lower() == 'clear':
            agent.clear_context()
            print("对话上下文已清空！\n")
            continue
        
        if query.lower() == 'change_image':
            new_path = input("请提供新的皮肤图像路径：").strip()
            if new_path and os.path.exists(new_path):
                agent.set_image(new_path)
                print(f"已更换图像: {os.path.basename(new_path)}\n")
            else:
                print("文件不存在\n")
            continue
        
        if not query:
            continue

        if debug_mode:
            print("\n" + "="*60)
            print("🔍 智能体决策过程")
            print("="*60)
            print(f"\n📌 用户输入: {query}")
            
            has_image = agent.context.get("image_path") is not None
            task_type = agent.determine_task_type(query, has_image)
            print(f"\n📌 任务类型: {task_type.value}")
            print(f"📌 当前阶段: {agent.current_stage.value}")
        
        print("\nAI: ", end="", flush=True)

        try:
            for chunk in agent.execute_stream(query):
                print(chunk, end="", flush=True)
                
            if debug_mode:
                print("\n" + "-"*40)
                print(f"📋 诊断阶段: {agent.current_stage.value}")
                
                if agent.context.get("diagnosis_result"):
                    print(f"✅ 图像诊断完成")
                if agent.context.get("treatment_result"):
                    print(f"✅ 治疗建议生成完成")
                    
        except Exception as e:
            logger.error(f"诊断过程出错: {e}")
            print(f"\n诊断过程出错: {e}")

        print()


if __name__ == '__main__':
    main()
    print()
    print("=" * 50)
    print("免责声明：以上结果仅供参考，不能替代专业医生诊断。")
    print("   如有疑虑，请及时就医。")
    print("=" * 50)
