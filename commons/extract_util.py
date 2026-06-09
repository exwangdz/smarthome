
"""
@Time ： 2024/11/29 17:51
@Auth ： eilert
@File ：extract_util.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Description ：提取变量工具类的封装，实现变量的跨py文件提取和使用
"""
import copy
import re
from string import Template
import jsonpath
import yaml

from commons.yaml_util import write_yaml, read_all
from hotload.debug_talk import DebugTalk


class ExtractUtil:

    #解析提取变量
    def extract_variable(self,res,var_name,attr_name,expr,index):

        #深拷贝(对原对象的地址拷贝，新拷贝了一份和原对象不同地址的对象，修改新对象的值不会影响到原对象的值)
        #浅拷贝（对原对象的值拷贝，地址仍然是指向同一个地址，修改拷贝的对象会改变原对象的值）
        new_res=copy.deepcopy(res)
        #把json()方法改成json属性
        try:
            new_res.json=new_res.json()
        except Exception:
            new_res.json={'msg':'resopnse is not json data'}

        #通过反射获取属性的值
        data=getattr(new_res,attr_name)
        # print("data: %s" % data)

        #判断通过什么提取方式提取数据
        if expr.startswith("$"):
            lis=jsonpath.jsonpath(dict(data),expr)
        else:
            lis=re.findall(expr,data)
        #通过下标取值并写入extract.yaml文件
        if lis:
            write_yaml({var_name:lis[index]})

    #解析使用变量,把$access_token替换成从extract_yaml中提取到的值
    def change(self,request_data: dict):
        #1把字典转成字符串
        data_str=yaml.safe_dump(request_data)
        #字符串替换
        # new_request_data=Template(data_str).safe_substitute(read_all())
        new_request_data = self.hotload_replace(data_str)
        #2把字符串还原成字典
        data_dict=yaml.safe_load(new_request_data)
        return data_dict
        pass

    def hotload_replace(self,data_str:str):
        #定义一个正则匹配的表达式
        regexp="\\$\\{(.*?)\\}"  #匹配${token}这种方式
        regexp = "\\$\\{(.*?)\\((.*?)\\)\\}" #匹配${函数名（参数)}这种方式
        #通过正则表达式在data_str字符串中去匹配，得到所有的表达式list
        fun_list=re.findall(regexp,data_str)
        #循环遍历fun_list
        for fun in fun_list:
            pass
            if fun[1]=="":  #没有参数
                new_value=getattr(DebugTalk(),fun[0])()
            else:  #有参数,有1～n个参数
                new_value=getattr(DebugTalk(),fun[0])(*fun[1].split(","))
            #如果value是一个数字格式的字符串
            if isinstance(new_value,str) and new_value.isdigit():
                new_value="'"+new_value+"'"
            #拼接旧的值
            old_value="${"+fun[0]+"("+fun[1]+")}"
            #把旧的表达式替换成函数返回的新的值
            data_str=data_str.replace(old_value,str(new_value))
        return data_str
#


if __name__ == '__main__':
    request_data={"method":"get","url":"http://www.baidu.com","data":"${read_yaml(number)}","params":"{$add(1,2)}","json":"{$get_random_number()}"}
    data_str=yaml.safe_dump(request_data)
    data_str=ExtractUtil().hotload_replace(data_str)



