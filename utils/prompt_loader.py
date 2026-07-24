"""
读取外部独立文本提示词文件
"""
from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


def load_system_prompts():
    """加载全局系统提示词"""
    try:
        # 获取配置文件中的文件路径参数得到完整路径
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置项中没有main_prompt_path配置项")
        raise e

    try:
        # 读取文件内容
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"[load_system_prompts]解析系统提示词出错, {str(e)}")
        raise e


def load_rag_prompts():
    """加载 RAG 检索总结提示词"""
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置项中没有rag_summarize_prompt_path配置项")
        raise e

    try:
        with open(rag_prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析RAG总结提示词出错, {str(e)}")


def load_report_prompts():
    """加载报告生成提示词"""
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml配置项中没有report_prompt_path配置项")
        raise e

    try:
        with open(report_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[load_report_prompts]解析报告生成提示词出错，{str(e)}")
        raise e


"""
# 优化写法
def load_prompt_by_key(config_key: str, desc: str):
    try:
        file_path = get_abs_path(prompts_conf[config_key])
    except KeyError as e:
        logger.error(f"[{desc}]yaml缺少配置项 {config_key}")
        raise e
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[{desc}]读取提示词失败：{str(e)}")
        raise e

# 调用
def load_system_prompts():
    return load_prompt_by_key("main_prompt_path", "系统提示词")

def load_rag_prompts():
    return load_prompt_by_key("rag_summarize_prompt_path", "RAG总结提示词")

def load_report_prompts():
    return load_prompt_by_key("report_prompt_path", "报告生成提示词")
"""

if __name__ == '__main__':
    print(load_report_prompts())    # 输出文件内容
