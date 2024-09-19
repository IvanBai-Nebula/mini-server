from django.db import models
from public.models import BaseModel


class Role(BaseModel):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True, null=False, blank=False)

    class Meta:
        db_table = 'role'
