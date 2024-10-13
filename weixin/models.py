from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from pages.models import Unit
from questions.models import Set
from utils.base_model import BaseModel


class CustomerUser(AbstractUser):
    """
    微信用户
    """

    openid = models.CharField(max_length=50, primary_key=True)  # 微信用户唯一标识
    username = models.CharField(max_length=150, unique=True)
    avatar = models.CharField(max_length=255, blank=True)  # 头像允许为空
    phone = models.CharField(max_length=20, unique=True, blank=True)  # 可用于后期的手机号登陆
    is_active = models.BooleanField(default=True)  # 默认激活

    def __str__(self):
        return self.username or self.openid


class Profile(BaseModel):
    """
    个人信息
    """

    height = models.IntegerField(blank=True, validators=[MinValueValidator(0), MaxValueValidator(300)])  # 身高范围0-300厘米
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True,
                                 validators=[MinValueValidator(0.0), MaxValueValidator(300.0)])  # 体重范围0-300公斤
    age = models.IntegerField(blank=True, validators=[MinValueValidator(0), MaxValueValidator(120)])
    blood_pressure = models.CharField(max_length=255, blank=True)
    blood_sugar = models.CharField(max_length=255, blank=True)
    blood_fat = models.CharField(max_length=255, blank=True)

    # 外键
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='profile', db_index=True)

    def __str__(self):
        return (self.user.username, self.height, self.weight, self.age,
                self.blood_pressure, self.blood_sugar, self.blood_fat, self.updated_at)


class SleepQuality(BaseModel):
    """
    睡眠质量
    """

    sleep_quality = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])

    # 外键
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='sleep_quality',
                             db_index=True)

    def __str__(self):
        return self.user.username, self.sleep_quality, self.updated_at

# class Collections(BaseModel):
#     """
#     定义收藏表
#     """
#
#     collection_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(WechatUser, on_delete=models.CASCADE, related_name='user_collections',
#                              db_index=True)
#     unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_collections')
#
#     class Meta:
#         db_table = 'collections'
#
#
# class BrowsingHistory(BaseModel):
#     """
#     定义浏览历史
#     """
#
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(WechatUser, on_delete=models.CASCADE, related_name='user_browsing_history',
#                              db_index=True)
#     unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_browsing_history')
#
#     class Meta:
#         db_table = 'browsing_history'
#
#
# class Leaderboard(BaseModel):
#     """
#     定义排行榜
#     """
#
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(WechatUser, on_delete=models.CASCADE, db_index=True)
#     set = models.ForeignKey(Set, on_delete=models.CASCADE)
#     total_answers = models.IntegerField()
#     total_score = models.IntegerField()
#     correctness = models.FloatField()
#
#     class Meta:
#         db_table = 'leaderboard'
