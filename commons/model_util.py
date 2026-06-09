"""
@Time ： 2024/11/29 17:51
@Auth ： eilert
@File ：model_util.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Description ：校验yaml测试用例
"""
from dataclasses import dataclass

from commons.request_util import logger


@dataclass
class CaseInfo:
    #必填
    feature: str
    story: str
    title: str
    request: dict
    validate: dict
    # paramtrize: list

    #选填
    extract: dict = None
    parametrize: list = None

#校验测试用例
# def verify_yaml(caseinfo:dict,yaml_name):
#     try:
#         if isinstance(caseinfo, CaseInfo):
#             return caseinfo
#         else:
#            new_caseinfo = CaseInfo(**caseinfo)
#            return new_caseinfo
#     except Exception:
#         logger.error(yaml_name+":YAML测试用例不符合框架规范")
#         raise Exception("YAML测试用例不符合框架规范")
def verify_yaml(caseinfo: dict, yaml_name):
    try:
        if isinstance(caseinfo, CaseInfo):
            return caseinfo
        else:
            case_data = caseinfo.copy()
            # 保存参数化数据（可能字段名为 _params 或 params_data）
            params_context = case_data.pop('_params', None) or case_data.pop('params_data', None)
            # 只保留 CaseInfo 构造函数接受的参数
            allowed_keys = {'feature', 'story', 'title', 'request', 'extract', 'validate'}
            filtered_data = {k: v for k, v in case_data.items() if k in allowed_keys}
            new_caseinfo = CaseInfo(**filtered_data)
            if params_context:
                new_caseinfo.params_context = params_context  # 挂载动态属性供后续使用
            return new_caseinfo
    except Exception as e:
        logger.error(f"{yaml_name}: YAML测试用例不符合框架规范, 错误: {e}")
        raise Exception("YAML测试用例不符合框架规范")


if __name__ == '__main__':
    a={
        'feature': '登录',
        'story': '获取鉴权码接口',
        'title': '获取鉴权码成功',
        'request': {
            'method': 'get',
            'url': 'https: // api.weixin.qq.com / cgi - bin / token',
            'params': {
              'grant_type': 'client_credential',
              'appid': 'wx8a9de038e93f77ab',
              'secret': '8326fc915928dee3165720c910effb86'}},
        'validate': 'null'


    }
    new_caseinfo= verify_yaml(a,yaml_name="test_aget_token.yaml")
    print(new_caseinfo)