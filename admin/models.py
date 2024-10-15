import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
class User(AbstractUser):
    """
    后台管理员
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    password = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, unique=True, db_index=True)  # 后期可以用于短信验证登陆等功能
    email = models.EmailField(max_length=255, unique=True, db_index=True)  # 邮箱验证注册或者重置密码
    avatar = models.URLField(max_length=255, blank=True)
    private_key = models.TextField(blank=True)
    is_staff = models.BooleanField(default=True)  # 管理员权限默认开启
    is_active = models.BooleanField(default=True)  # 默认激活

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_groups',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_permissions',
        related_query_name='user',
    )

    def __str__(self):
        return f"""
                id:{self.id},
                username:{self.username},
                email:{self.email},
                phone:{self.phone},
                is_staff:{self.is_staff},
                is_active:{self.is_active},
                date_joined:{self.date_joined},
                """


def generate_default_phone():
    last_user = User.objects.order_by('-id').first()
    if last_user:
        last_phone = last_user.phone or ''
        try:
            last_number = int(last_phone.split('-')[-1])
            new_number = last_number + 1
        except ValueError:
            new_number = 1
        return f'default-{new_number}'
    return 'default-1'


@receiver(pre_save, sender=User)
def set_default_phone(sender, instance, **kwargs):
    if not instance.phone:
        instance.phone = generate_default_phone()
