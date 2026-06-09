
"""
@Time ： 2024/11/29 17:51
@Auth ： eilert
@File ：assert_util.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Description ：数据驱动的封装
"""
import yaml

from commons.request_util import logger


#读取测试用例

def read_testcase(yaml_path):
    with open(yaml_path,encoding="utf-8") as f:
        case_list=yaml.safe_load(f)
        if len(case_list)>=2:  #多接口用例:{},{},{}]
           return case_list #返回“[[{},{},{}]]”
        else:
            if  "parametrize" in dict(*case_list).keys():  #带有parametrize数据驱动[{}]
                new_caseinfo=ddts(*case_list,yaml_path.name)
                return new_caseinfo   #"数据驱动用例,[返回{正例},{反例},{反例}]"
            else:
               return case_list #"单口用例":返回[{}]

def ddts(caseinfo:dict, yaml_name):  #将带有 parametrize 字段的单个用例字典，根据数据驱动表展开成多个独立用例字典
    #数据驱动：把一个{}返回“[{正例},{反例},{反例}]”
    data_list=caseinfo["parametrize"]
    len_flag=True
    name_len=len(data_list[0]) #获取第一个参数的长度
    for data in data_list:

      if len(data)!= name_len:
        len_flag=False
        logger.error(yaml_name+":parametrize数据驱动用例的参数个数不一致!\n")
        break
      if not len_flag:
        return []

   #如果长度没有问题
    str_caseinfo=yaml.dump(caseinfo)
    new_caseinfo=[]
    if len_flag:
        for x in range (1,len(data_list)): #x表示行，行从下标为1开始
            raw_caseinfo=str_caseinfo
            for y in range(0,name_len): #y表示列，列从下标为0开始
                #如果是数据类型的字符串则需要加上一个单引号
                if isinstance(data_list[x][y],str) and data_list[x][y].isdigit():
                    data_list[x][y]="'"+data_list[x][y]+"'"
                raw_caseinfo=raw_caseinfo.replace("$ddt{"+data_list[0][y]+"}",str(data_list[x][y]))
            case_dict=yaml.safe_load(raw_caseinfo)
            case_dict.pop("parametrize")
            new_caseinfo.append(case_dict)
    return new_caseinfo


#数据驱动运行原理
#1、读取yaml测试用例,利用yaml.safe_load()方法，把yaml文件转换成python对象
#2、判断是否是数据驱动用例
#3、如果是数据驱动用例，则返回“[{正例},{反例},{反例}]”，再通过parametrize进行解包成字典传入执行
#4、如果不是数据驱动用例，则返回[{}]#单接口
#5、如果是多接口用例，则返回“[[{},{},{}]]”
#6、如果不是多接口用例，则返回[{}] #单接口
#7、如果是单接口用例，则返回[{}] #单接口


