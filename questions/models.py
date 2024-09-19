from django.db import models

from public.models import BaseModel


# Create your models here.
class Set(BaseModel):
    set_id = models.AutoField(primary_key=True)
    set_title = models.CharField(max_length=255, unique=True, null=False, blank=False)
    set_image = models.CharField(max_length=255)
    set_description = models.TextField(null=True)

    class Meta:
        db_table = 'set'

    def __str__(self):
        return f"{self.set_id}: {self.set_title}"


class question(BaseModel):
    question_id = models.AutoField(primary_key=True)
    set_id = models.ForeignKey(Set, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
