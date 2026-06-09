from pathlib import Path
import jsonpath
import pytest
import allure
from commons.extract_util import ExtractUtil
from commons.main_util import standard_case_flow
from commons.model_util import verify_yaml
from commons.request_util import RequestUtil, logger
from commons.yaml_util import read_testcase, write_yaml
eu=ExtractUtil()
class TestAllCase:
    pass

#根据一个yaml的路径·创建一个测试用例的函数并且返回这个函数

def create_testcase(yaml_path):
    @pytest.mark.parametrize("caseinfo", read_testcase(yaml_path))
    def func(self, caseinfo):
        global case_object
        if isinstance(caseinfo,list): #多接口用例
            for case in caseinfo:
                logger.info("YAML测试用例路径：%s" % yaml_path)
                #校验yaml文件
                case_object = verify_yaml(case,yaml_path.name)
                #用标准化用例流程
                standard_case_flow(case_object,yaml_path)
        else: #单接口用例
            logger.info("YAML测试用例路径：%s" % yaml_path)
              #校验yaml文件
            case_object = verify_yaml(caseinfo,yaml_path.name)
            #调用标准化用例流程
            standard_case_flow(case_object,yaml_path)
        # #定制allure报告
        # allure.dynamic.feature(case_object.feature)
        # allure.dynamic.story(case_object.story)
        # allure.dynamic.title(case_object.title)
    return func
#循环获取所有的yaml文件(一个yaml文件生成一个用例，然后把用例放到类下面)
testcase_path = Path(__file__).parent
yaml_case_list = list((testcase_path / "data").glob("*.yaml"))
# testcase_path=Path(__file__).parent  #获取testcase的路径
# yaml_case_list=testcase_path.glob("**/*.yaml")
#用例执行顺序的处理
yaml_case_list=list((testcase_path / "data").glob("*.yaml"))
yaml_case_list.sort()
for  yaml_path in yaml_case_list:
     print(yaml_path)
     print(yaml_path.stem)
     create_testcase(yaml_path)
     #通过反射，这个循环每循环一次就生成一个函数，然后把这个函数加到TestAllCase类下面
     setattr(TestAllCase,"test_"+yaml_path.stem,create_testcase(yaml_path))



if __name__ == '__main__':
   pytest.main()

#框架运行原理
#1通过pytest.ini文件寻找testcase目录下以test_*py开头的文件
#2通过寻找test_*py文件中的类名以Test开头的类
#3通过先循环获取所有的yaml文件(这个循环每循环一次就生成一个函数，然后把这个函数加到TestAllCase类下面)
#4通过寻找类中的方法名以test开头的函数（用例）
#5当执行到第一用例时就会读取对应的YAML文件的内容，然后对YAML文件做校验（verify_yaml）看用例是否有问题，没有问题则会
#生成一个对象(new_caseinfo)，将对象里面的内容（请求四要素）进行解包后发送请求，执行用例