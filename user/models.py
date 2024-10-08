from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from utils.models import BaseModel
from role.models import Role
from media.models import Unit
from questions.models import Set


# 定义用户模型
class User(BaseModel):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)  # 用于后台管理登陆使用
    password = models.CharField(max_length=255, null=True, blank=True)  # 用于后台管理登陆使用
    avatar = models.CharField(max_length=255, null=True, blank=True)  # 头像允许为空
    openid = models.CharField(max_length=255, unique=True, null=True, blank=True)  # 用户唯一标识
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="电话号码格式不正确")
    phone = models.CharField(max_length=255, unique=True, null=True, blank=True, validators=[phone_validator])  # 添加验证
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user'  # 数据库表名


# 定义睡眠质量的选择项
SLEEP_QUALITY_CHOICES = (
    ('1', '优'),
    ('2', '良'),
    ('3', '中'),
    ('4', '差'),
)


# 定义用户信息模型
# 用户信息模型继承自BaseModel，包含了用户的详细信息如昵称、头像、身高、体重等。
# 所有字段都允许为空或空白。
class UserInfo(BaseModel):
    id = models.AutoField(primary_key=True)  # 自动递增的主键
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_info')  # 关联用户信息
    height = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                 validators=[MinValueValidator(0.00), MaxValueValidator(3.00)])  # 身高范围0-3米
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True,
                                 validators=[MinValueValidator(0.0), MaxValueValidator(300.0)])  # 体重范围0-300公斤
    age = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(120)])  # 年龄范围
    blood_pressure = models.CharField(max_length=255, null=True, blank=True)  # 血压范围允许为空
    blood_sugar = models.CharField(max_length=255, null=True, blank=True)  # 血糖范围允许为空
    blood_fat = models.CharField(max_length=255, null=True, blank=True)  # 血脂范围允许为空
    sleep_quality = models.CharField(max_length=10, choices=SLEEP_QUALITY_CHOICES, null=True, blank=True)  # 睡眠质量允许为空

    class Meta:
        db_table = 'user_info'  # 数据库表名


# 定义收藏模型
# 收藏模型继承自BaseModel，记录了用户收藏的内容。
class Collections(BaseModel):
    collection_id = models.AutoField(primary_key=True)  # 自动递增的主键
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_collections', db_index=True)  # 关联用户信息
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_collections')  # 关联媒体内容

    class Meta:
        db_table = 'collections'  # 数据库表名


# 定义浏览历史模型
# 浏览历史模型继承自BaseModel，记录了用户的浏览记录。
class BrowsingHistory(BaseModel):
    id = models.AutoField(primary_key=True)  # 自动递增的主键
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_browsing_history',
                             db_index=True)  # 关联用户信息
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_browsing_history')  # 关联媒体内容

    class Meta:
        db_table = 'browsing_history'  # 数据库表名


# 定义排行榜模型
# 排行榜模型继承自BaseModel，记录了用户的答题情况。
class Leaderboard(BaseModel):
    id = models.AutoField(primary_key=True)  # 自动递增的主键
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # 关联用户信息
    set = models.ForeignKey(Set, on_delete=models.CASCADE)  # 关联问题集
    total_answers = models.IntegerField()  # 总答题数
    total_score = models.IntegerField()  # 总得分
    correctness = models.FloatField()  # 正确率

    class Meta:
        db_table = 'leaderboard'  # 数据库表名


# 定义聊天记录模型
class ChatRecord(BaseModel):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', db_index=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    image = models.CharField(max_length=255)

    class Meta:
        db_table = 'chat_record'
