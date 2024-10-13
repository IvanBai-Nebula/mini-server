from django.db import models
from utils.base_models import BaseModel


# 定义类别模型
class Category(BaseModel):
    id = models.AutoField(primary_key=True)
    parent = models.IntegerField(default=0)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, db_index=True)

    class Meta:
        db_table = 'category'


# 定义文章模型
class Article(BaseModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(null=True)

    class Meta:
        db_table = 'article'


# 定义视频模型
class Video(BaseModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True)
    url = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'video'


# 定义内容单元模型
class Unit(BaseModel):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='units')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name='units')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True, related_name='units')
    title = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'unit'


class MediaFile(models.Model):
    id = models.AutoField(primary_key=True)
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ]
    title = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='uploads/')  # 文件将上传到 media/uploads 路径

    class Meta:
        db_table = 'media_file'

    def __str__(self):
        return self.title
