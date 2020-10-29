from django.db import models

# 日志
class OperationLogs(models.Model):
    type = models.CharField(default='info', max_length=64, verbose_name="日志类型")
    content = models.TextField(verbose_name="修改详情", null=True)
