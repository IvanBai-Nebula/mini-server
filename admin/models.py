import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
class AdminUser(AbstractUser):
    """
    后台管理员
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    password = models.CharField(max_length=150)
    avatar = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, unique=True, db_index=True)  # 后期可以用于短信验证登陆等功能
    is_staff = models.BooleanField(default=True)  # 管理员权限默认开启
    is_active = models.BooleanField(default=True)  # 默认激活

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='admin_user_groups',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='admin_user_permissions',
        related_query_name='user',
    )

    class Meta:
        db_table = 'admin_user'

    def __str__(self):
        return self.username


def generate_default_phone():
    last_user = AdminUser.objects.order_by('-id').first()
    if last_user:
        last_phone = last_user.phone or ''
        try:
            last_number = int(last_phone.split('-')[-1])
            new_number = last_number + 1
        except ValueError:
            new_number = 1
        return f'default-{new_number}'
    return 'default-1'


@receiver(pre_save, sender=AdminUser)
def set_default_phone(sender, instance, **kwargs):
    if not instance.phone:
        instance.phone = generate_default_phone()
