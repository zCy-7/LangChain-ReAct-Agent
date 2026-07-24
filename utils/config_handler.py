"""
加载配置文件, 读取全局变量

YAML 是一种人类可读的配置文件格式，全称 YAML Ain't Markup Language，专门用来写配置、数据，比 JSON、XML 更简洁易读。
文件后缀：.yaml / .yml
"""
import yaml
from utils.path_tool import get_abs_path


def load_rag_config(
        config_path: str = get_abs_path("config/rag.yml"),
        encoding: str = "utf-8"
):
    with open(config_path, 'r', encoding=encoding) as f:
        # return yaml.load(f, loader=yaml.FullLoader)   # 版本不兼容
        return yaml.full_load(f)


def load_prompts_config(
        config_path: str = get_abs_path("config/prompts.yml"),
        encoding: str = "utf-8"
):
    with open(config_path, 'r', encoding=encoding) as f:
        return yaml.full_load(f)


def load_chroma_config(
        config_path: str = get_abs_path("config/chroma.yml"),
        encoding: str = "utf-8"
):
    with open(config_path, 'r', encoding=encoding) as f:
        return yaml.full_load(f)


def load_agent_config(
        config_path: str = get_abs_path("config/agent.yml"),
        encoding: str = "utf-8"
):
    with open(config_path, 'r', encoding=encoding) as f:
        return yaml.full_load(f)


# # 通用写法, 避免写四遍
# def load_config(file_name: str, encoding: str = "utf-8"):
#     path = get_abs_path(f"config/{file_name}.yml")
#     with open(path, "r", encoding=encoding) as f:
#         return yaml.full_load(f)
#
#
# # 使用
# rag_conf = load_config("rag")
# chroma_conf = load_config("chroma")


rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()


if __name__ == '__main__':
    print(rag_conf["chat_model_name"])      # 读取配置文件中的 chat_model_name 信息
    print(type(rag_conf["chat_model_name"]))
