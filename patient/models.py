from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.base_model import BaseModel
from weixin.models import CustomerUser


class Info(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    birthday = models.DateField(blank=True)  # 前端自行转成年龄
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices)
    height = models.IntegerField(blank=True)  # cm
    weight = models.DecimalField(max_digits=4, decimal_places=1)  # kg
    pulse = models.IntegerField(blank=True)  # 心率
    blood_pressure = models.CharField(max_length=20, blank=True)  # 收缩压/舒张压 mmHg
    blood_sugar = models.DecimalField(max_digits=3, decimal_places=1, blank=True)  # mmHg
    blood_fat = models.DecimalField(max_digits=3, decimal_places=1, blank=True)  # mmHg
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name="patients")

    def __str__(self):
        return f"""
                id:{self.id},
                name:{self.name},   
                birthday:{self.birthday},
                gender:{self.gender},
                height:{self.height},
                weight:{self.weight},
                pulse:{self.pulse},
                blood_pressure:{self.blood_pressure},
                blood_sugar:{self.blood_sugar},
                blood_fat:
                """
