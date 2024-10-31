from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from utils.base_model import BaseModel


class CustomerUser(AbstractUser):
    """
    微信用户
    """

    id = models.CharField(max_length=50, primary_key=True)  # 由openid微信用户唯一标识
    username = models.CharField(max_length=150, unique=True)
    avatar = models.CharField(max_length=255, blank=True)  # 头像可以为空，使用前端默认头像
    phone = models.CharField(max_length=20, unique=True, blank=True)  # 可用于后期的手机号登陆
    is_active = models.BooleanField(default=True)  # 默认激活

    def __str__(self):
        return f"""
                id:{self.id},
                username:{self.username},
                phone:{self.phone},
                is_active:{self.is_active},
                date_joined:{self.date_joined}
                """

    @classmethod
    def create_user(cls, **kwargs):
        user = cls(
            id=kwargs.get('openid'),
            username=kwargs.get('username', f"WX-{kwargs['openid']}"),
            phone=kwargs.get('phone', ''),
            avatar=kwargs.get('avatar', ''),
            is_active=True,
            password=make_password(None)  # 设置一个不可用的密码
        )
        user.save()
        return user


def generate_default_phone():
    """
    生成默认手机号
    """

    last_user = CustomerUser.objects.order_by('-pk').first()
    if last_user:
        last_phone = last_user.phone or ''
        try:
            last_number = int(last_phone.split('-')[-1])
            new_number = last_number + 1
        except ValueError:
            new_number = 1
        return f'default-{new_number}'
    return 'default-1'


@receiver(pre_save, sender=CustomerUser)
def set_default_phone(sender, instance, **kwargs):
    """
    在保存CustomerUser实例之前，如果username未设置，则使用默认手机号。
    """

    if not instance.phone:
        instance.phone = generate_default_phone()


class Profile(BaseModel):
    """
    个人信息
    """

    height = models.IntegerField(blank=True)  # cm
    weight = models.DecimalField(max_digits=4, decimal_places=1)  # kg
    birthday = models.DateField(blank=True)  # 前端自行转成年龄
    blood_pressure = models.CharField(max_length=20, blank=True)  # 收缩压/舒张压 mmHg
    blood_sugar = models.DecimalField(max_digits=3, decimal_places=1, blank=True)  # mmHg
    blood_fat = models.DecimalField(max_digits=3, decimal_places=1, blank=True)  # mmHg

    # 外键
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='profile', db_index=True)

    def __str__(self):
        return f"""
                username:{self.user.username},
                height:{self.height},
                weight:{self.weight},
                birthday:{self.birthday},
                blood_pressure:{self.blood_pressure},
                blood_sugar:{self.blood_sugar},
                blood_fat:{self.blood_fat},
                updated_at:{self.updated_at}
                """


class SleepQuality(BaseModel):
    """
    睡眠质量
    """

    sleep_quality = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])

    # 外键
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='sleep_quality',
                             db_index=True)

    def __str__(self):
        return f"""
                id:{self.id},
                user:{self.user.username},
                sleep_quality:{self.sleep_quality},
                updated_at:{self.updated_at}
                """

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
