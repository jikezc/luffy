from django.db import models

class BaseModel(models.Model):
    '''公共模型'''
    orders = models.IntegerField(verbose_name='显示顺序')
    is_show = models.BooleanField(verbose_name="是否上架", default=False)
    is_delete = models.BooleanField(verbose_name="逻辑删除", default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 设置当前模型为抽象模型，在django执行数据迁移时，不会为当前模型创建表和迁移文件
        abstract = True
