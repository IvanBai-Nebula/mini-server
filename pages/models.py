from django.db import models

from utils.base_model import BaseModel


# 定义类别模型
class Category(BaseModel):
    parent = models.IntegerField(default=0)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, db_index=True)


# 定义文章模型
class Article(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(null=True)


# 定义视频模型
class Video(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True)
    url = models.CharField(max_length=255, null=False, blank=False)


# 定义内容单元模型
class Unit(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='units')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name='units')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True, related_name='units')
    title = models.CharField(max_length=255, null=False, blank=False)


class MediaFile(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ]
    title = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='uploads/')  # 文件将上传到 pages/uploads 路径

    def __str__(self):
        return self.title
