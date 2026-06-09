"""
@Time ： 2024/11/29 17:51
@Auth ： eilert
@File ：yaml_util.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Description ：yaml文件读取方法的封装
"""

# import yaml
#
# #读取yaml文件
# def read_yaml(key):
#     with open("extract.yaml",encoding="utf-8") as f:
#         value=yaml.safe_load(f)
#     return value[key]
#
# #写入yaml文件
# def write_yaml(data):
#     with open("extract.yaml", encoding="utf-8", mode='a') as f:
#          yaml.safe_dump(data,f,allow_unicode=True)
#
#
# #清空yaml文件
# def clean_yaml():
#     with open("extract.yaml", encoding="utf-8", mode='w') as f:
#         pass
#
#
#
# def read_testcase(yaml_path):
#     with open(yaml_path,encoding="utf-8") as f:
#         value=yaml.safe_load(f)
#     return value
#
# #读取extract.yaml文件中所有的值
# def read_all():
#     with open('extract.yaml', encoding="utf-8") as f:
#         value=yaml.safe_load(f)
#     return value


import yaml
import copy
import os
import re
from pathlib import Path
def read_yaml(key):
    with open("extract.yaml", encoding="utf-8") as f:
        value = yaml.safe_load(f)
    if value is None:
        return None
    return value.get(key)  # 改用 get 避免 KeyError


#
# def write_yaml(data):
#     # 注意：改为覆盖写入，避免重复；通常建议保存所有提取变量为字典后再整体写入
#     # 这里简单处理：读取原有内容，合并后写入
#     try:
#         with open("extract.yaml", encoding="utf-8") as f:
#             existing = yaml.safe_load(f) or {}
#     except FileNotFoundError:
#         existing = {}
#     existing.update(data)
#     with open("extract.yaml", encoding="utf-8", mode='w') as f:
#         yaml.safe_dump(existing, f, allow_unicode=True)
def write_yaml(data: dict):
    file_path = "extract.yaml"
    existing = {}
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            existing = yaml.safe_load(f) or {}
    existing.update(data)
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(existing, f)

def clean_yaml():
    with open("extract.yaml", encoding="utf-8", mode='w') as f:
        pass


def read_testcase(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not isinstance(data, list):
        data = [data]

    expanded_cases = []
    for case in data:
        if 'parametrize' in case:
            params_list = case.pop('parametrize')
            for params in params_list:
                new_case = copy.deepcopy(case)

                # 递归替换 request 中的所有字符串占位符
                def replace_placeholders(obj):
                    if isinstance(obj, dict):
                        return {k: replace_placeholders(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [replace_placeholders(item) for item in obj]
                    elif isinstance(obj, str):
                        # 匹配 $xxx 形式的占位符
                        def replacer(match):
                            var_name = match.group(1)
                            return str(params.get(var_name, match.group(0)))

                        return re.sub(r'\$(\w+)', replacer, obj)
                    else:
                        return obj

                new_case['request'] = replace_placeholders(new_case.get('request', {}))
                # 注意：extract 中的表达式可能也包含占位符，但通常不需要替换
                expanded_cases.append(new_case)
        else:
            expanded_cases.append(case)
    return expanded_cases

def _expand_case(case_meta):
    """
    如果 case_meta 中有 paramtrize 字段，则根据参数列表生成多个用例副本。
    每个副本添加 '_params' 字段存放当前组的参数值。
    """
    if 'paramtrize' not in case_meta:
        return [case_meta]

    param_list = case_meta.pop('paramtrize')  # 取出参数化列表
    expanded = []
    for idx, params in enumerate(param_list):
        new_case = copy.deepcopy(case_meta)
        new_case['_params'] = params  # 存储当前组的参数值
        # 可选：修改 title 以区分不同数据组
        if 'title' in new_case:
            new_case['title'] = f"{new_case['title']}_data{idx + 1}"
        expanded.append(new_case)
    return expanded


def read_all():
    with open('extract.yaml', encoding="utf-8") as f:
        value = yaml.safe_load(f) or {}
    return value