"""
@Time ： 2024/11/29 17:51
@Auth ： eilert
@File ：base_url.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Description ：多环境基础路径的处理
"""
from iniconfig import IniConfig


def read_ini():
    ini=IniConfig("../pytest.ini")
    if "base_url" not in ini:
        return  {}
    else:
        return dict(ini["base_url"].items())


if __name__ == '__main__':
    print(read_ini())