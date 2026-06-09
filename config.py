import os
from pathlib import Path


class Config:
    # 基础路径
    BASE_DIR = Path(__file__).parent.absolute()

    # 接口配置
    BASE_URL = "https://api.weixin.qq.com/cgi-bin/token?"
    LOG_LEVEL = "DEBUG"
    LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s"
    LOG_DIR = BASE_DIR / "logs"

    # 测试数据
    TEST_DATA_DIR = BASE_DIR / "testcases/data"


# 初始化时创建必要目录
Config.LOG_DIR.mkdir(exist_ok=True)
(Config.BASE_DIR / "reports/allure-results").mkdir(parents=True, exist_ok=True)



#运行测试
# pytest --alluredir=./reports/allure-results
#
# #生成报告
# allure serve ./reports/allure-results


class TestConfig(Config):
    BASE_DIR =  "testcases"
    # 测试数据
    BASE_URL = "https//:www.baidu.com"
    #日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(astime)s | %(levelname)-8s | %(name)-25s | %(message)s"