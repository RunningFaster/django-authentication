from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from mptt.models import MPTTModel

from basic.base_model import BaseModel


class UserBase(BaseModel):
    """
    用户信息
    """
    username = models.CharField("用户名", max_length=50, unique=True)
    password = models.CharField("密码", max_length=128)
    name = models.CharField("昵称", max_length=50)
    SEX = (
        (0, "女"),
        (1, "男"),
        (2, "未知"),
    )
    sex = models.IntegerField(choices=SEX, default=1, blank=True)
    mobile = models.CharField("手机", max_length=11, default="", blank=True)
    email = models.EmailField("邮箱", null=True, blank=True)
    head_image = models.FileField(upload_to="image/%Y/%m", default="", max_length=1024, blank=True, null=True,
                                  verbose_name="头像")
    IS_ACTIVE = (
        (0, "停用"),
        (1, "正常")
    )
    is_active = models.IntegerField("状态", choices=IS_ACTIVE, default=1, blank=True)
    # 一个用户只能属于一个部门
    department = models.ForeignKey(
        "Department", on_delete=models.SET_DEFAULT, blank=True, default=1, verbose_name="部门")
    # 一个用户可以拥有多个角色
    role = models.ManyToManyField("Role", related_name="user_base")
    remark = models.CharField("备注", max_length=200, blank=True, default="")

    # 在重写Django默认User模型时，需要当前三个属性
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str(self):
        return self.username

    objects = UserManager()

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        get_latest_by = "create_datetime"
        ordering = ['create_datetime']
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["mobile"]),
            models.Index(fields=["department"]),
        ]

    @staticmethod
    def set_password(raw_password):
        return make_password(raw_password)

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn"t be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    # 在重写Django默认User模型时，需要引用此方法
    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    # 在重写Django默认User模型时，需要引用此方法
    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def get_role_list(self):
        # 查询当前用户所拥有的角色
        return self.role.all()

    def get_menus_list(self):
        # 查询当前用户所拥有的权限
        roles = self.get_role_list()
        menu_list = sum([list(role.menu.all()) for role in roles], [])
        return list(set([i for i in menu_list]))

    def get_permission_api_list(self):
        # 查询当前用户能操作的的api列表
        roles = self.get_role_list()
        api_list = []
        for role in roles:
            menus = list(role.menu.all())
            for menu in menus:
                if menu.type != 2:
                    continue
                # 从内存中取出查询的缓存信息
                api_list += menu.apis if hasattr(menu, "apis") else menu.api
        return list(set(api_list))

    def get_permission_department_list(self):
        # 查询当前用户所能操作的部门的权限
        roles = self.get_role_list()
        department_list = []
        for role in roles:
            department_list += role.departments if hasattr(role, "departments") else role.department
        return department_list


class Api(BaseModel):
    name = models.CharField("接口名称", max_length=200)
    path = models.CharField("接口地址", max_length=200, db_index=True)
    format_path = models.CharField("格式化接口地址", max_length=200, default="", blank=True, db_index=True)
    method = models.CharField("方法", max_length=200)
    is_common = models.IntegerField("是否通用接口", default=0, blank=True)
    remark = models.CharField("备注", max_length=300, default="", blank=True)

    def __str(self):
        return self.name

    class Meta:
        verbose_name = "api接口表"
        verbose_name_plural = verbose_name


class Menu(BaseModel):
    name = models.CharField("节点名称", max_length=200)
    icon = models.CharField("节点图标", max_length=100, blank=True, default="")
    is_show = models.IntegerField("是否显示", default=1, blank=True)
    order_num = models.IntegerField("排序号", default=0, blank=True, help_text="0-99数值越小，顺序越靠前", db_index=True)
    TYPE = (
        (0, "目录"),
        (1, "菜单"),
        (2, "权限"),
    )
    type = models.IntegerField("类型", choices=TYPE)
    is_keep_alive = models.IntegerField("页面是否缓存", default=1, blank=True)
    path = models.CharField("路由地址", max_length=200, blank=True, default="")
    view_path = models.CharField("文件路径", max_length=200, blank=True, default="")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="父级对象")
    api = models.ManyToManyField(Api, related_name="menu")

    def __str(self):
        return self.name

    class Meta:
        verbose_name = "权限表"
        verbose_name_plural = verbose_name


class Department(BaseModel):
    name = models.CharField("名称", max_length=200)
    nick_name = models.CharField("别名", max_length=200, blank=True, null=True)
    full_name = models.CharField("全称", max_length=200, blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL,
                               blank=True, null=True,
                               verbose_name="父级对象",
                               related_name="children")

    def __str(self):
        return self.name

    class Meta:
        verbose_name = "部门表"
        verbose_name_plural = verbose_name


class Role(BaseModel):
    name = models.CharField("名称", max_length=200, unique=True, db_index=True, help_text="角色名称唯一，admin为超级管理员")
    label = models.CharField("标识", max_length=200)
    remark = models.CharField("备注", max_length=200, blank=True, default="")
    menu = models.ManyToManyField(Menu, related_name="role")
    """
    角色和部门的关系，如果当前角色没有分配任何一个部门的数据权限，则默认为只查询与自身相关的
    部门的配置信息，需要配置到最底层，在数据的过滤中，会根据最基础信息进行
    数据的过滤，是根据不同的业务需求进行过滤。。
    考虑到的情况是：一个小组长新增了一个业务数据，把这个数据分配给了小组下的某个员工，则该员工也能查看到当前数据，其他员工无法查看数据
    """
    department = models.ManyToManyField(Department, related_name="department")

    def __str(self):
        return self.name

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = verbose_name
        ordering = ['create_datetime']
