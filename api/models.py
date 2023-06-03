from django.db import models

# Create your models here.
class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name='用户名',max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)
    role = models.CharField(verbose_name='角色',max_length=32,default='管理员')
    def __str__(self):
        return self.username


class Students(models.Model):
    """学生表"""
    name=models.CharField(verbose_name='姓名',max_length=32)
    studentId = models.BigIntegerField(verbose_name='学号')
    college = models.CharField(verbose_name='学院', max_length=32)
    major = models.CharField(verbose_name='专业', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    sex_choies = (
        (0,'女'),
        (1,'男')
    )
    sex = models.IntegerField(verbose_name='性别',choices=sex_choies)
    role = models.CharField(verbose_name='角色', max_length=32,default='学生')
    def __str__(self):
        return self.name



class Teachers(models.Model):
    """教师表"""
    name=models.CharField(verbose_name='姓名',max_length=32)
    teacherId = models.BigIntegerField(verbose_name='教职工号')
    college = models.CharField(verbose_name='学院', max_length=32)
    itro = models.CharField(verbose_name='教师介绍', max_length=32,blank=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    phone = models.CharField(verbose_name='教师电话', max_length=64)
    sex_choies = (
        (0,'女'),
        (1,'男')
    )
    sex = models.IntegerField(verbose_name='性别',choices=sex_choies)
    role = models.CharField(verbose_name='角色',max_length=32,default='教师')
    def __str__(self):
        return self.name


class Topic(models.Model):
    """论文表"""
    title = models.CharField(verbose_name='论文标题', max_length=32)
    teacherName = models.ForeignKey(to="Teachers",on_delete=models.CASCADE,verbose_name='教师姓名')
    topicDirect = models.CharField(verbose_name='论文方向', max_length=32)
    maxNum = models.IntegerField(verbose_name='限定人数')


