"""
从配置文件中读取不同场景的提示词文件路径，并加载对应的提示词内容，支持系统提示词，RAG提示词和报告提示词
"""

from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger import logger


#加载系统提示词
def load_system_prompts():
    try:
        system_prompts_path = get_abs_path(prompts_conf["main_prompt_path"])

    except KeyError as e:
        logger.error(f'[load_system_prompts]在yaml中未找到main_prompt_path配置项')
        raise e





    try:
        return open(system_prompts_path,"r",encoding="utf-8").read()

    except Exception as e:
        logger.error(f'[load_system_prompts]在加载系统提示词时发生错误:{e}')
        raise e






#加载RAG总结提示词
def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])

    except KeyError as e:
        logger.error(f'[load_rag_prompts]在yaml中未找到rag_summarize_prompt_path配置项')
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()

    except Exception as e:
        logger.error(f'[load_rag_prompts]解析RAG提示词出错,{str(e)}')
        raise e




#加载报告生成提示词
def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f'[load_report_prompts]在yaml中未找到report_prompt_path配置项')
        raise e


    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()

    except Exception as e:
        logger.error(f'[load_report_prompts]解析报告生成提示词出错,{str(e)}')
        raise e




if __name__ == '__main__':
    print(load_report_prompts())












