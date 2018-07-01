from django.shortcuts import render
from base.models import Project, Sign, Env, Case, Plan, Report, Api
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.core import serializers
from lib.execute import Execute
import time
import json
# Create your views here.


# 项目增删改查
def project_index(request):
    prj_list = Project.objects.all()
    return render(request, "base/project/index.html", {"prj_list": prj_list})


def project_add(request):
    if request.method == 'POST':
        prj_name = request.POST['prj_name']
        name_same = Project.objects.filter(prj_name=prj_name)
        if name_same:
            messages.error(request, "项目已存在")
        else:
            description = request.POST['description']
            sign_id = request.POST['sign']
            sign = Sign.objects.get(sign_id=sign_id)
            prj = Project(prj_name=prj_name, description=description, sign=sign)
            prj.save()
            return HttpResponseRedirect("/base/project/")
    sign_list = Sign.objects.all()
    return render(request, "base/project/add.html", {"sign_list": sign_list})


def project_update(request):
    if request.method == 'POST':
        prj_id = request.POST['prj_id']
        prj_name = request.POST['prj_name']
        name_exit = Project.objects.filter(prj_name=prj_name).exclude(prj_id=prj_id)
        if name_exit:
            messages.error(request, "项目已存在")
            # return HttpResponse("项目已存在")
        else:
            description = request.POST['description']
            sign_id = request.POST['sign_id']
            sign = Sign.objects.get(sign_id=sign_id)
            Project.objects.filter(prj_id=prj_id).update(prj_name=prj_name, description=description,sign=sign)
            return HttpResponseRedirect("/base/project/")
    prj_id = request.GET['prj_id']
    prj = Project.objects.get(prj_id=prj_id)
    sign_list = Sign.objects.all()
    return render(request, "base/project/update.html", {"prj": prj, "sign_list": sign_list})

def project_delete(request):
    if request.method == 'GET':
        prj_id = request.GET['prj_id']
        Project.objects.filter(prj_id=prj_id).delete()
        return HttpResponseRedirect("base/project/")



# 加密方式增删改查
def sign_index(request):
    sign_list = Sign.objects.all()
    return render(request, "system/sign_index.html", {"sign_list": sign_list})

def sign_add(request):
    if request.method == 'POST':
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        sign = Sign(sign_name=sign_name, description=description)
        sign.save()
        return HttpResponseRedirect("/base/sign/")
    return render(request, "system/sign_add.html")

# 更新加密方式
def sign_update(request):
    if request.method == 'POST':
        sign_id = request.POST['sign_id']
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        Sign.objects.filter(sign_id=sign_id).update(sign_name=sign_name, description=description)
        return HttpResponseRedirect("/base/sign/")
    sign_id = request.GET['sign_id']
    sign = Sign.objects.get(sign_id=sign_id)
    return render(request, "system/sign_update.html", {"sign": sign})


# 测试环境增删改查
def env_index(request):
    env_list = Env.objects.all()
    return render(request, "base/env/index.html", {"env_list": env_list})


def env_add(request):
    if request.method == 'POST':
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        private_key = request.POST['private_key']
        description = request.POST['description']
        env = Env(env_name=env_name, url=url, project=project,
                  private_key=private_key, description=description)
        env.save()
        return HttpResponseRedirect("/base/env/")
    prj_list = Project.objects.all()
    return render(request, "base/env/add.html", {"prj_list": prj_list})
# 测试环境更新
def env_update(request):
    if request.method == 'POST':
        env_id = request.POST['env_id']
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        private_key = request.POST['private_key']
        description = request.POST['description']
        Env.objects.filter(env_id=env_id).update(env_name=env_name, url=url, project=project, private_key=private_key, description=description)
        return HttpResponseRedirect("/base/env/")
    env_id = request.GET['env_id']
    env = Env.objects.get(env_id=env_id)
    prj_list = Project.objects.all()
    return render(request, "base/env/update.html", {"env": env, "prj_list": prj_list})


# 接口增删改查
def api_index(request):
    api_list = Api.objects.all()
    return render(request, "api/index.html", {"api_list": api_list})


def api_add(request):
    if request.method == 'POST':
        if_name = request.POST['if_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        method = request.POST['method']
        data_type = request.POST['data_type']
        is_sign = request.POST['is_sign']
        description = request.POST['description']
        request_header_data = request.POST['request_header_data']
        request_body_data = request.POST['request_body_data']
        response_header_data = request.POST['response_header_data']
        response_body_data = request.POST['response_body_data']
        api = Api(if_name=if_name, url=url, project=project, method=method, data_type=data_type,
                          is_sign=is_sign, description=description, request_header_param=request_header_data,
                          request_body_param=request_body_data, response_header_param=response_header_data,
                          response_body_param=response_body_data)
        api.save()
        return HttpResponseRedirect("/base/interface/")
    prj_list = Project.objects.all()
    return render(request, "base/interface/add.html", {"prj_list": prj_list})

"""
# 接口增删改查
def interface_index(request):
    if_list = Interface.objects.all()
    return render(request, "base/interface/index.html", {"if_list": if_list})

def interface_add(request):
    if request.method == 'POST':
        if_name = request.POST['if_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        method = request.POST['method']
        data_type = request.POST['data_type']
        is_sign = request.POST['is_sign']
        description = request.POST['description']
        request_header_data = request.POST['request_header_data']
        request_body_data = request.POST['request_body_data']
        response_header_data = request.POST['response_header_data']
        response_body_data = request.POST['response_body_data']
        interface = Interface(if_name=if_name, url=url, project=project, method=method, data_type=data_type,
                          is_sign=is_sign, description=description, request_header_param=request_header_data,
                          request_body_param=request_body_data, response_header_param=response_header_data,
                          response_body_param=response_body_data)
        interface.save()
        return HttpResponseRedirect("/base/interface/")
    prj_list = Project.objects.all()
    return render(request, "base/interface/add.html", {"prj_list": prj_list})
"""


# 接口增删改查
def case_index(request):
    case_list = Case.objects.all()
    return render(request, "base/case/index.html", {"case_list": case_list})

def case_add(request):
    if request.method == 'POST':
        case_name = request.POST['case_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        description = request.POST['description']
        content = request.POST['content']
        case = Case(case_name=case_name, project=project, description=description, content=content)
        case.save()
        return HttpResponseRedirect("/base/case/")
    prj_list = Project.objects.all()
    return render(request, "base/case/add.html", {"prj_list": prj_list})

def case_run(request):
    if request.method == 'POST':
        case_id = request.POST['case_id']
        env_id = request.POST['env_id']
        execute = Execute(case_id, env_id)
        case_result = execute.run_case()
        return JsonResponse(case_result)


# 计划增删改查
def plan_index(request):
    plan_list = Plan.objects.all()
    return render(request, "base/plan/index.html", {"plan_list": plan_list})

def plan_add(request):
    if request.method == 'POST':
        plan_name = request.POST['plan_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        env_id = request.POST['env_id']
        environment = Env.objects.get(env_id=env_id)
        description = request.POST['description']
        content = request.POST.getlist("case_id")
        plan = Plan(plan_name=plan_name, project=project, environment=environment, description=description, content=content)
        plan.save()
        return HttpResponseRedirect("/base/plan/")
    prj_list = Project.objects.all()
    return render(request, "base/plan/add.html", {"prj_list": prj_list})

def plan_run(request):
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        plan = Plan.objects.get(plan_id=plan_id)
        env_id = plan.environment.env_id
        case_id_list = eval(plan.content)
        case_num = len(case_id_list)
        content = []
        pass_num = 0
        fail_num = 0
        error_num = 0
        for case_id in case_id_list:
            execute = Execute(case_id, env_id)
            case_result = execute.run_case()
            content.append(case_result)
            if case_result["result"] == "pass":
                pass_num += 1
            if case_result["result"] == "fail":
                fail_num += 1
            if case_result["result"] == "error":
                error_num += 1
        report_name = plan.plan_name + "-" + time.strftime("%Y%m%d%H%M%S")
        if Report.objects.filter(plan=plan):
            Report.objects.filter(plan=plan).update(report_name=report_name, content=content, case_num=case_num,
                                                    pass_num=pass_num, fail_num=fail_num, error_num=error_num)
        else:
            report = Report(plan=plan, report_name=report_name, content=content, case_num=case_num,
                            pass_num=pass_num, fail_num=fail_num, error_num=error_num)
            report.save()
        return HttpResponse(plan.plan_name + " 执行成功！")


def report_index(request):
    plan_id = request.GET['plan_id']
    report = Report.objects.get(plan_id=plan_id)
    report_content = eval(report.content)
    return render(request, "report.html", {"report": report, "report_content": report_content})


def findata(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        get_type = request.GET["type"]
        if get_type == "get_all_if_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 返回字典列表
            if_list = Api.objects.filter(project=prj_id).all().values()
            # list(if_list)将QuerySet转换成list
            return JsonResponse(list(if_list), safe=False)
        if get_type == "get_if_by_if_id":
            if_id = request.GET["if_id"]
            # 查询并将结果转换为json
            interface = Api.objects.filter(if_id=if_id).values()
            return JsonResponse(list(interface), safe=False)
        if get_type == "get_env_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            env = Env.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(env), safe=False)
        if get_type == "get_all_case_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            env = Case.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(env), safe=False)