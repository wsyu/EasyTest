#!/usr/bin/python
# coding:utf-8
__author__ = 'wsy'

from modules import Sign, Project, Environment, APIDoc, Case, db_session
import requests
import hashlib
import re
import json
from handlers.system.base import BaseHandler
from lib.signtype import *

class Execute():
    def __init__(self, case_id, env_id):
        self.db_session = db_session
        self.case_id = case_id
        self.env_id = env_id
        self.glo_var = {}
        self.pro_id, self.env_url, self.private_key = self.get_env(self.env_id)
        self.sign_type = self.get_sign(self.pro_id)
        self.step_json = []

    def run_case(self):
        case = self.db_session.query(Case).filter(Case.id == self.case_id).first()
        step_list = eval(case.content)
        case_result = {"result": "pass"}
        case_result["case_id"] = self.case_id
        case_result["case_name"] = case.case_name
        step_result_list = []
        for step in step_list:
            step_result = self.step(step)
            step_result_list.append(step_result)
            if step_result["result"] == "fail":
                case_result["result"] = "fail"
        db_session.close()
        case_result["step_list"] = step_result_list
        return case_result


    def step(self, step_content):
        step = {}
        var_list = self.extract_variables(step_content)
        if var_list:
            for var_name in var_list:
                var_value = self.get_param(var_name, step_content)
                if var_value is None:
                    var_value = self.get_param(var_name, self.step_json)
                step_content = json.loads(self.replace_var(step_content, var_name, var_value))

        sendheader, sendate, res = self.call_interface(api_id=step_content["api_id"], url=step_content["api_url"],
                                  header=step_content["header"],
                                  data=step_content["body"])

        if step_content["extract"]:
                step_content = self.get_extract(step_content, res)
                self.step_json.append(step_content)
        if step_content["validators"]:
                result, msg = self.validators_result(step_content, res.text)
        else:
            result = "pass"
            msg = {}
        step["api_id"] = step_content["api_id"]
        step["api_name"] = step_content["api_name"]
        step["url"] = res.url
        step["send_header"] = sendheader
        step["send_data"] = sendate
        step["res_status_code"] = res.status_code
        step["res_content"] = res.text
        step["result"] = result
        step["msg"] = msg
        return step

    # 验证结果
    def validators_result(self, content, res):
        result = ""
        msg = []
        if isinstance(content, str):
            content = json.loads(content)
        if content["validators"]:
            validators_list = content["validators"]
            for var_field in validators_list:
                validator = {}
                check_filed = var_field["check"]
                expect_filed = var_field["expect"]
                check_filed_value = self.get_param(check_filed, res)
                validator["check_filed"] = check_filed
                validator["check_filed_value"] = check_filed_value
                validator["expect_filed"] = expect_filed
                msg.append(validator)
                if check_filed_value == expect_filed:
                    result = "pass"
                else:
                    result = "fail"
                    break
        return result, msg

    # 在response中提取参数, 并返回
    def get_extract(self, step_content, res):
        if step_content["extract"]:
            for key, value in step_content["extract"].items():
                key_value = self.get_param(key, res.text)
                step_content["extract"][key] = key_value
        return step_content


    # 替换内容中的变量, 返回字符串型
    def replace_var(self, content, var_name, var_value):
        if not isinstance(content, str):
            content = json.dumps(content)
        var_name = "$" + var_name
        content = content.replace(str(var_name), str(var_value))
        return content



    # 从内容中提取所有变量名, 变量格式为$variable,返回变量名list
    def extract_variables(self, content):
        variable_regexp = r"\$([\w_]+)"
        if not isinstance(content, str):
            content = str(content)
        try:
            return re.findall(variable_regexp, content)
        except TypeError:
            return []

    # 在内容中获取某一参数的值
    def get_param(self, param, content):
        param_val = None
        if isinstance(content, str):
            # content = json.loads(content)
            try:
                content = json.loads(content)
            except:
                content = ""
        if isinstance(content, dict):
            param_val = self.get_param_reponse(param, content)
        if isinstance(content, list):
            dict_data = {}
            for i in range(len(content)):
                try:
                    dict_data[str(i)] = eval(content[i])
                except:
                    dict_data[str(i)] = content[i]
            param_val = self.get_param_reponse(param, dict_data)
        if param_val is None:
            return param_val
        else:
            if "$" + param == param_val:
                param_val = None
            return param_val
    """
    # 在reponse中获取某一参数的值
    def get_param(self, param, dict_data):
        if isinstance(json.loads(dict_data), dict):
            param_val = self.get_param_reponse(param, json.loads(dict_data))
        else:
            list_data = json.loads(dict_data)
            dict_data = {}
            for i in range(len(list_data)):
                try:
                    dict_data[str(i)] = json.loads(list_data[i])
                except:
                    dict_data[str(i)] = list_data[i]
            param_val = self.get_param_reponse(param, dict_data)
        return param_val
        """

    def get_param_reponse(self, param_name, dict_data, default=None):
        for k, v in dict_data.items():
            if k == param_name:
                return v
            else:
                if isinstance(v, dict):
                    ret = self.get_param_reponse(param_name, v)
                    if ret is not default:
                        return ret
                if isinstance(v, list):
                    for i in v:
                        if isinstance(i, dict):
                            ret = self.get_param_reponse(param_name, i)
                            if ret is not default:
                                return ret
                        else:
                            pass
        return default




    # 获取测试环境
    def get_env(self, env_id):
        env = self.db_session.query(Environment).filter(Environment.id == env_id).first()
        pro_id =env.pro_id
        env_url = env.url
        private_key = env.private_key
        return pro_id, env_url, private_key

    # 获取加密方式
    def get_sign(self, pro_id):
        """
        sign_type: 加密方式
        """
        pro = self.db_session.query(Project).filter(Project.id == pro_id).first()
        sign_type = pro.sign_id
        return sign_type


    # 发送请求
    def call_interface(self, api_id, url, data, header):


        api = self.db_session.query(APIDoc).filter(APIDoc.id == api_id).first()
        url = self.env_url + url
        method = api.method
        content_type = api.data_type
        data = get_sendata(self.sign_type, data, self.private_key)
        if method == "post":
            if content_type == "json":
                r = requests.post(url=url, json=data, headers=header, verify=False)
            if content_type == "data":
                print(url,data,header)
                r = requests.post(url=url, data=data, headers=header, verify=False)
        if method == "get":
            r = requests.get(url=url, params=data, headers=header, verify=False)
            """
            if content_type == "json":
                r = requests.get(url=url, json=data, headers=header, verify=False)
            if content_type == "data":
                r = requests.get(url=url, data=data, headers=header, verify=False)
                """
        return header, data, r

