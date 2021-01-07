from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class BaseModel(models.Model):
    create_datetime = models.DateTimeField("新增时间", auto_now_add=True, editable=False, db_index=True)
    create_user = models.IntegerField("创建者", blank=True)
    update_datetime = models.DateTimeField("最新修改时间", auto_now=True, editable=False, db_index=True)
    update_user = models.IntegerField("修改者", blank=True)

    class Meta:
        abstract = True


class UserBase(BaseModel):
    username = models.CharField("用户名", max_length=50, unique=True)
    password = models.CharField("密码", max_length=128)
    name = models.CharField("昵称", max_length=50)
    SEX = (
        (0, "女"),
        (1, "男"),
        (2, "未知"),
    )
    sex = models.IntegerField(choices=SEX, default=1, blank=True)
    mobile = models.CharField("手机", max_length=11, null=True, blank=True)
    email = models.EmailField("邮箱", null=True, blank=True)
    head_image = models.FileField(upload_to="image/%Y/%m", default="", max_length=1024, blank=True, null=True,
                                  verbose_name="头像")
    IS_ACTIVE = (
        (0, "停用"),
        (1, "正常")
    )
    is_active = models.IntegerField("状态", choices=IS_ACTIVE, default=1, blank=True)
    # 行政区域
    city = models.CharField("市", max_length=50, default="上海市", blank=True)
    city_id = models.CharField("城市id", max_length=10, default="3101", blank=True)
    district = models.CharField("区县", max_length=50, default="", blank=True)
    district_id = models.CharField("区县id", max_length=10, default="", blank=True)
    street = models.CharField("街道", max_length=50, default="", blank=True)
    street_id = models.CharField("街道id", max_length=10, default="", blank=True)
    committee = models.CharField("居委", max_length=50, default="", blank=True)
    committee_id = models.CharField("居委id", max_length=10, default="", blank=True)
    grid = models.CharField("网格", max_length=50, default="", blank=True, help_text="如果属于多个网格，使用,进行拼接")

    department = models.CharField("部门对象", max_length=10, null=True, blank=True)

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


class Api(BaseModel):
    name = models.CharField("接口名称", max_length=200)
    path = models.CharField("接口地址", max_length=200, db_index=True)
    format_path = models.CharField("格式化接口地址", max_length=200, default="", blank=True, db_index=True)
    method = models.CharField("方法", max_length=200)
    is_common = models.IntegerField("是否通用接口", default=0, blank=True)
    remark = models.CharField("备注", max_length=300, default="", blank=True)
    MODE = (
        (0, "仅本人"),
        (1, "仅本部门"),
        (2, "全部"),
        (3, "自定义"),
    )
    mode = models.IntegerField("数据授权范围", choices=MODE, default=1, blank=True)

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
    parent_id = models.IntegerField("父级对象", blank=True, default=0)

    def __str(self):
        return self.name

    class Meta:
        verbose_name = "权限表"
        verbose_name_plural = verbose_name


class MenuApi(BaseModel):
    menu = models.IntegerField("权限", db_index=True)
    api = models.IntegerField("接口", db_index=True)

    def __str(self):
        return str(self.menu) + "/" + str('api')

    class Meta:
        verbose_name = "权限接口表"
        verbose_name_plural = verbose_name


class Role(BaseModel):
    name = models.CharField("名称", max_length=200, unique=True, db_index=True, help_text="角色名称唯一，admin为超级管理员")
    label = models.CharField("标识", max_length=200)
    remark = models.CharField("备注", max_length=200, blank=True, default="")

    def __str(self):
        return self.name

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = verbose_name


class RoleDepartment(BaseModel):
    role = models.IntegerField("角色", db_index=True)
    department = models.IntegerField("部门", db_index=True)

    class Meta:
        verbose_name = "角色部门表"
        verbose_name_plural = verbose_name


class RoleUserBase(BaseModel):
    role = models.IntegerField("角色", db_index=True)
    user_base = models.IntegerField("用户", db_index=True)

    def __str(self):
        return str(self.user_base) + "/" + str(self.role)

    class Meta:
        verbose_name = "用户角色表"
        verbose_name_plural = verbose_name


class RoleMenu(BaseModel):
    role = models.IntegerField("角色", db_index=True)
    menu = models.IntegerField("权限", db_index=True)

    def __str(self):
        return str(self.menu) + "/" + str(self.role)

    class Meta:
        verbose_name = "角色权限表"
        verbose_name_plural = verbose_name


class Department(BaseModel):
    name = models.CharField("名称", max_length=200)
    nick_name = models.CharField("别名", max_length=200, blank=True, null=True)
    full_name = models.CharField("全称", max_length=200, blank=True, null=True)
    parent_id = models.IntegerField("父级对象", blank=True, null=True)

    def __str(self):
        return self.name

    class Meta:
        verbose_name = "部门表"
        verbose_name_plural = verbose_name


class Event(BaseModel):
    name = models.CharField("名称", max_length=200)
    department = models.IntegerField("部门", db_index=True, help_text="当前数据来源于哪个部门")
    parent_id = models.IntegerField("父级对象", blank=True, null=True)

    class Meta:
        verbose_name = "事件表"
        verbose_name_plural = verbose_name


# 区
class District(models.Model):
    name = models.CharField("名称", max_length=128, unique=True)
    district_code = models.CharField("区的code", max_length=32, unique=True)

    create_time = models.DateTimeField("create time", auto_now_add=True)
    update_time = models.DateTimeField("update time", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "metadata_district"
        verbose_name = "区数据"
        verbose_name_plural = verbose_name


# 街道
class Street(models.Model):
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="区")
    name = models.CharField("街镇名称", max_length=128, unique=True)  # this will fix it
    street_code = models.CharField("街道的code", max_length=32, unique=True)

    nick_name = models.CharField("别名", max_length=512)  # this will fix it
    username = models.CharField("用户", max_length=255, default="", db_index=True)  # this will fix it
    create_time = models.DateTimeField("create time", auto_now_add=True)
    update_time = models.DateTimeField("update time", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "metadata_street"
        verbose_name = "街镇数据"
        verbose_name_plural = verbose_name


# 居委
class Committee(models.Model):
    is_delete = models.TextField(blank=True, null=True)  # 是否删除
    district_id = models.TextField(blank=True, null=True)  # 区id
    district_name = models.TextField("区名称", blank=True, null=True)
    town_id = models.TextField(blank=True, null=True)  # 街道id
    town_name = models.TextField("街道名称", blank=True, null=True)
    name = models.CharField("居委名称", max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "metadata_committee"
        verbose_name = "居委数据"
        verbose_name_plural = verbose_name
