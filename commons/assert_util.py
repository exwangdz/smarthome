
"""
@Time ： 2024/11/29 17:51
@Auth ： eilert
@File ：assert_util.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
@Description ：断言工具类的封装
"""

import copy
import pymysql

from configs import setting


class AssertUtil:
    #链接数据库
    def conn_database(self):
        self.conn=pymysql.connect(
            user=setting.db_username,
            password=setting.db_password,
            host=setting.db_host,
            port=setting.db_port,
            database=setting.db_database
        )
        return self.conn

    #执行SQL语句
    def execute_sql(self,sql):
        #创建链接
        conn=self.conn_database()
        #创建游标
        cursor=conn.cursor()
        #执行SQL语句
        cursor.execute(sql)
        #获取结果
        result=cursor.fetchone()
        #关闭游标
        cursor.close()
        #关闭链接
        conn.close()
        return result

    def assert_all_case(self, res, assert_type, value):
        # 深拷贝一个res
        new_res = copy.deepcopy(res)
        # 把json()方法改成json属性
        try:
            new_res.json = new_res.json()
        except Exception:
            new_res.json = {'msg': 'response is not json data'}

        # 根据断言类型分别处理
        if assert_type == "equals":
            for msg, yq_and_sj_data in value.items():
                yq, sj = yq_and_sj_data[0], yq_and_sj_data[1]
                # 获取实际值
                try:
                    sj_value = getattr(new_res, sj)
                except AttributeError:
                    # 若属性不存在，尝试从响应 JSON 中获取
                    if isinstance(new_res.json, dict) and sj in new_res.json:
                        sj_value = new_res.json[sj]
                    else:
                        sj_value = sj
                assert yq == sj_value, msg

        elif assert_type == "contains":
            # value 是列表，例如：[["access_token", "text"]]
            for item in value:
                if len(item) != 2:
                    continue
                yq, sj = item[0], item[1]  # yq: 期望字符串，sj: 数据源（text/json/属性名）
                # 获取实际值
                if sj == "text":
                    sj_value = new_res.text
                elif sj == "json":
                    sj_value = str(new_res.json)
                else:
                    try:
                        sj_value = getattr(new_res, sj)
                    except Exception:
                        sj_value = sj
                # 默认消息
                msg = f"期望响应中包含 '{yq}'，但未找到"
                assert yq in sj_value, msg

        elif assert_type == "db_equals":
            for msg, yq_and_sj_data in value.items():
                yq, sj = yq_and_sj_data[0], yq_and_sj_data[1]
                yq_value = self.execute_sql(yq)
                assert yq_value[0] == sj, msg

        elif assert_type == "db_contains":
            for msg, yq_and_sj_data in value.items():
                yq, sj = yq_and_sj_data[0], yq_and_sj_data[1]
                yq_value = self.execute_sql(yq)
                assert yq_value[0] in sj, msg

        else:
            raise ValueError(f"不支持的断言类型: {assert_type}")

    # def assert_all_case(self, res, assert_type, value):
    #     #深拷贝一个res
    #     new_res= copy.deepcopy(res)
    #     #把json()方法改成json属性
    #     try:
    #         new_res.json = new_res.json()
    #     except Exception:
    #         new_res.json = {'msg': 'resopnse is not json data'}
    #     #循环判断断言类型
    #     for msg,yq_and_sj_data in value.items():
    #         yq,sj= yq_and_sj_data[0],yq_and_sj_data[1]
    #         #根据属性获取到属性的值
    #         try:
    #              sj_value=getattr(new_res,sj)
    #         except Exception:
    #              sj_value=sj
    #         #断言
    #         match assert_type:
    #             case "equals":
    #                 assert yq==sj_value,msg
    #             case "contains":
    #                 assert yq in sj_value,msg
    #
    #             case "db_equals":
    #                 yq_value = self.execute_sql(yq)
    #                 assert yq_value[0]==sj_value, msg
    #
    #             case "db_contains":
    #                 yq_value=self.execute_sql(yq)
    #                 assert yq_value[0] in sj_value,msg

if __name__ == '__main__':
    value=AssertUtil().execute_sql('select * from pw_user')
    print(value)