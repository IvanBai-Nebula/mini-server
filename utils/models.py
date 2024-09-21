from django.db import models
from utils.manager import BaseManager


# Create your models here.

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
