from django.db import models


# Create your models here.

class BaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)  # 默认只查询未删除的对


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        ordering = ['-updated_at']
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """ Soft delete the object instead of actually deleting it. """
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])
