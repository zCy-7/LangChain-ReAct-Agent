"""为整个项目提供统一的绝对路径"""
import os


def get_project_root() -> str:
    """获取项目所在的根目录"""
    # 1. 获取当前文件的绝对路径
    current_path = os.path.abspath(__file__)        # D:\PythonProject\Agent项目案例\utils\path_tool.py
    # 2. 获取当前目录的上一级目录
    previous_path = os.path.dirname(current_path)   # D:\PythonProject\Agent项目案例\utils
    # 3. 获取项目根目录
    root_path = os.path.dirname(previous_path)      # D:\PythonProject\Agent项目案例

    return root_path


def get_abs_path(relative_path: str) -> str:
    """
    传递相对路径,返回绝对路径
    Args:
        relative_path: 相对路径
    Returns: 绝对路径
    """
    root_path = get_project_root()

    return os.path.join(root_path, relative_path).replace('\\', '/')
    # return os.path.join(root_path, relative_path)


if __name__ == '__main__':
    # get_project_root()
    # print(os.path.abspath(__file__))

    # path = get_abs_path("abc.py")
    # print(path)     # D:\PythonProject\Agent项目案例\abc.py
    path = get_abs_path("config/chroma.yml")
    print(path)   # # D:/PythonProject/Agent项目案例/config/chroma.yml
