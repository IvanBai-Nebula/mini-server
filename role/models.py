from django.db import models
from utils.models import BaseModel


class Role(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, null=False, blank=False)

    class Meta:
        db_table = 'role'
