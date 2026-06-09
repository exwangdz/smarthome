
"""
热加载（在yaml文件中调用python方法）
"""
import base64
import hashlib
import time
import rsa
import yaml

from commons.base_url import read_ini


class DebugTalk:

    def read_yaml(self, key):
        with open("extract.yaml", encoding="utf-8") as f:
            value = yaml.safe_load(f) or {}  # 使用4个空格（或一个Tab）缩进
        return value.get(key)  # 注意这行与 with 对齐，不属于 with 块y)
    #
    # def read_yaml(self,key):
    #  with open("extract.yaml",encoding="utf-8") as f:
    #     value=yaml.safe_load(f)
    #  return value[key]

    def env(self,key):
        return read_ini()[key]

    def add(self,a,b):
        return a+b

    def get_random_number(self):
        return str(int(time.time()*1000))

    def md5_code(self,data):
        #把data转化成utf-8编码
        data=str(data).encode("utf-8")
        #md5加密,哈希算法
        md5_value=hashlib.md5(data).hexdigest()
        return md5_value

    def base64_encode(self,data):
       # 把data转化成utf-8编码
       data = str(data).encode("utf-8")
       # base64加密
       base64_value = base64.b64encode(data).decode(encoding="utf-8")
       return base64_value

    #生成RSA公钥和私钥
    def create_key(self):
        (public_key, private_key) = rsa.newkeys(1024)
        return public_key,private_key






if __name__ == '__main__':
     print(DebugTalk().base64_encode("admin"))

