"""
皮肤病诊断Agent启动入口
"""
import sys
import os
import json
from agent.react_agent import SkinDiagnosisAgent
from utils.logger import logger
 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HISTORY_FILE = "conversation_history.json"


def main():
    print("=" * 50)
    print("     皮肤疾病诊断助手")
    print("=" * 50)
    print("命令：")
    print("  'quit' / 'exit' - 退出程序")
    print("  'save' - 保存对话历史")
    print("  'clear' - 清空历史")
    print()
    
    print("正在初始化诊断系统...\n")
    agent = SkinDiagnosisAgent()
    
    if os.path.exists(HISTORY_FILE):
        load_choice = input("发现历史对话，是否加载？(y/n): ").strip().lower()
        if load_choice == 'y':
            count = agent.load_history(HISTORY_FILE)
            if count > 0:
                print(f"已加载 {count} 条对话历史！\n")

    print("-" * 50)
    image_path = input("请提供皮肤图像路径：").strip()
    
    if image_path:
        agent.set_image(image_path)
        print(f"\n已加载图像，开始分析...\n")
    else:
        print("\n未提供图像，将以文字问答模式运行\n")

    print("-" * 50)
    print("AI: ", end="", flush=True)
    
    try:
        for chunk in agent.execute_stream("开始"):
            print(chunk, end="", flush=True)
    except Exception as e:
        logger.error(f"诊断过程出错: {e}")
        print(f"\n诊断过程出错: {e}")

    print()
    print("-" * 50)

    while True:
        query = input("\n您: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        if query.lower() == 'save':
            count = agent.save_history(HISTORY_FILE)
            print(f"对话历史已保存（共 {count} 条消息）")
            continue
        
        if query.lower() == 'clear':
            agent.clear_history()
            print("对话历史已清空！\n")
            continue
        
        if query.lower() == 'change_image':
            new_path = input("请提供新的皮肤图像路径：").strip()
            if new_path:
                agent.set_image(new_path)
                print(f"已更换图像: {new_path}\n")
            continue
        
        if not query:
            continue

        print("\nAI: ", end="", flush=True)

        try:
            for chunk in agent.execute_stream(query):
                print(chunk, end="", flush=True)
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
