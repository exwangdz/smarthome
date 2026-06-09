"""
@Time ： 2024/11/29 17:51
@Auth ： eilert
@File ：main_util.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Description ：用例标准化工具的封装
"""
import traceback
from commons.assert_util import AssertUtil
from commons.extract_util import ExtractUtil
from commons.model_util import verify_yaml
from commons.request_util import RequestUtil, logger

eu=ExtractUtil()
ru=RequestUtil()
au=AssertUtil()
#
def standard_case_flow(case_object,yaml_path):
    #把请求参数写入日志
    logger.info("模块>接口>用例：+str(case_object.feature)+">"+str(case_object.story)+">"+str(case_object.title")
    # 验证yaml文件
    case_object= verify_yaml(case_object,yaml_path)
    # 使用提取的值
    # new_request = eu.change(case_object.request)
    # 读取yaml文件中的请求四要素并发送请求
    print(case_object.request)
    # 发送请求
    res = ru.send_all_requests(**eu.change(case_object.request))
    # 请求之后得到响应后去提取变量
    if case_object.extract:
        for key, value in case_object.extract.items():
            # eu.extract_variable(res, key, *value)
            eu.extract_variable(res, key, value[0], value[1], 0)

    #请求之后得到响应后如果validate不为空，则需要断言
    try:
        if case_object.validate:
          for assert_type, value in eu.change(case_object.validate).items():
            au.assert_all_case(res, assert_type, value)
          logger.info("断言成功!\n")
        else:
           logger.warning("此用例没有断言!\n")
    except Exception as e:
        logger.error("断言失败！%s" % str(traceback.format_exc()))
        raise e





    # 断言
    if case_object.validate:
        for assert_type, assert_value in case_object.validate.items():
            au.assert_all_case(res, assert_type, assert_value)