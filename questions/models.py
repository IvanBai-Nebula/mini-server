from django.db import models

from utils.base_model import BaseModel


# Create your models here.
class Set(BaseModel):
    title = models.CharField(max_length=255, unique=True, null=False, blank=False)
    image = models.CharField(max_length=255)
    description = models.TextField(null=True)


class question(BaseModel):
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    set = models.ForeignKey(Set, on_delete=models.CASCADE)
