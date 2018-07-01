from django.db import models

# Create your models here.


class Sign(models.Model):
    sign_id = models.AutoField(primary_key=True, null=False, verbose_name="签名方式ID")
    sign_name = models.CharField(max_length=50, verbose_name="签名方式")
    description = models.CharField(max_length=100, verbose_name="描述")

    class Meta:
        verbose_name = "签名"
        verbose_name_plural = verbose_name
        db_table = "tb_sign"

    def __str__(self):
        return self.sign_name


class Project(models.Model):
    prj_id = models.AutoField(primary_key=True, null=False, verbose_name="项目ID")
    prj_name = models.CharField(max_length=50, null=False, verbose_name="项目名称")
    sign = models.ForeignKey('Sign', on_delete=models.CASCADE, verbose_name="加密方式")
    description = models.CharField(max_length=100, verbose_name="描述")

    class Meta:
        db_table = "tb_project"
        verbose_name = "项目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.prj_name


class Env(models.Model):
    env_id = models.AutoField(primary_key=True, null=False, verbose_name="ID")
    env_name = models.CharField(max_length=50, null=False, verbose_name="测试环境名称")
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name="所属项目")
    description = models.CharField(max_length=100, verbose_name="描述")
    url = models.CharField(max_length=100, verbose_name="URL")
    private_key = models.CharField(max_length=50, verbose_name="密钥")

    class Meta:
        db_table = "tb_env"
        verbose_name = "测试环境"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.env_name


class Api(models.Model):
    api_id = models.AutoField(primary_key=True, null=False, verbose_name="接口ID")
    api_name = models.CharField(max_length=50, null=False, verbose_name="接口名")
    api_url = models.CharField(max_length=50, verbose_name="访问地址")
    method = models.CharField(max_length=4, verbose_name="请求方式")
    data_type = models.CharField(max_length=4, verbose_name="数据传输方式")
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name="所属项目")
    is_sign = models.IntegerField(verbose_name="是否签名")
    description = models.CharField(max_length=100, verbose_name="描述")
    request_header_param = models.TextField()
    request_body_param = models.TextField()
    response_header_param = models.TextField()
    response_body_param = models.TextField()

    class Meta:
        db_table = "tb_api"
        verbose_name = "接口"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.api_name

"""
class Interface(models.Model):
    if_id = models.AutoField(primary_key=True, null=False)
    if_name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    method = models.CharField(max_length=4)
    data_type = models.CharField(max_length=4)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    is_sign = models.IntegerField()
    description = models.CharField(max_length=100)
    request_header_param = models.TextField()
    request_body_param = models.TextField()
    response_header_param = models.TextField()
    response_body_param = models.TextField()

    def __str__(self):
        return self.if_name
    """


class Case(models.Model):
    case_id = models.AutoField(primary_key=True, null=False, verbose_name="用例ID")
    case_name = models.CharField(max_length=50, verbose_name="用例名称")
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name="所属项目")
    description = models.CharField(max_length=200, verbose_name="描述")
    content = models.TextField(verbose_name="内容")

    class Meta:
        db_table = "tb_case"
        verbose_name = "用例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.case_name


class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True, null=False)
    plan_name = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    environment = models.ForeignKey('Env', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        db_table = "tb_plan"
        verbose_name = "测试计划"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.plan_name


class Report(models.Model):
    report_id = models.AutoField(primary_key=True, null=False)
    report_name = models.CharField(max_length=255)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    content = models.TextField()
    case_num = models.IntegerField(null=True)
    pass_num = models.IntegerField(null=True)
    fail_num = models.IntegerField(null=True)
    error_num = models.IntegerField(null=True)

    class Meta:
        db_table = "tb_report"
        verbose_name = "测试报告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.report_name