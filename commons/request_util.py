"""
@Time ： 2024/11/29 17:51
@Auth ： eilert
@File ：request_util.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Description ：requests请求工具类的封装
"""

import requests
import logging
from requests import Response
#生成日志对象
logger= logging.getLogger(__name__)

# from Api_Auto_Test.testcase.test_api import Testsendrequests


#统一请求封装(去除重复冗余的代码；跨py文件实现通过一个sess来自动关联有cookie关联的接口
# ；设置统一、公共参数，统一的文件处理，统一的异常处理，统一的日志监控，用例校验等)
class RequestUtil:
    # 创建一个requests.Session()对象
    sess=requests.Session()

    # 发送所有请求的方法
    def send_all_requests(self, method,url,**kwargs):
        # 使用requests.Session()对象发送请求
        #处理公共参数
        total_params={
            "access_token": "access_token"
        }
        for key,value in kwargs.items():
            if key=="params":
               kwargs['params'].update(total_params)
            try:
                 if key=="files":
                    for file_key,file_value in value.items():
                        value[file_key]=open(file_value,"rb")
            except Exception:
                  logger.error("请求参数有误")
              #把请求四要素写入日志
            logger.info("请求"+key+"参数:%s" % value)
        # #发送请求
        res=RequestUtil.sess.request(method, url,**kwargs)
        #判断返回的内容是否是一个json格式(目的是encode编码转换成中文)
        if "json" in res.headers.get("Content-Type"):
            logger.info("响应结果:%s" % res.json())
        else:
            logger.info("响应内容太长不显示在日志")
        # 返回请求结果
        return res