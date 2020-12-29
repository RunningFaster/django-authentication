from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    create_datetime = models.DateTimeField('新增时间', auto_now_add=True, editable=False, db_index=True)
    create_user = models.IntegerField('创建者', blank=True)
    update_datetime = models.DateTimeField('最新修改时间', auto_now=True, editable=False, db_index=True)
    update_user = models.IntegerField('修改者', blank=True)

    class Meta:
        abstract = True


# Create your models here.

class UserBase(BaseModel):
    username = models.CharField(u'用户名', max_length=50, unique=True)
    password = models.CharField(u'密码', max_length=128)
    nick_name = models.CharField(u'昵称', max_length=50)
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default='female', blank=True)
    mobile = models.CharField(u"手机", max_length=11, null=True, blank=True)
    image = models.FileField(upload_to="image/%Y/%m", default="image/default_head_image.jpg", max_length=100)
    is_active = models.BooleanField(u'状态', default=True, blank=True)
    remark = models.CharField(u'备注', max_length=200, blank=True, default='')
    _password = None

    def __str(self):
        return self.username

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.set_password(kwargs['password'])
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

#
# class Urls(BaseModel):
#     title = models.CharField(u"描述信息", max_length=200)
#     path = models.CharField(u"路由地址", max_length=200)
#     parent_id = models.IntegerField(u"父级对象", default=0, blank=True)
#
#     def __str(self):
#         return self.path
#
#     class Meta:
#         verbose_name = u"路由地址信息"
#         verbose_name_plural = verbose_name
