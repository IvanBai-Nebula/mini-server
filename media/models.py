from django.db import models

from public.models import BaseModel


# 定义类别模型
class Category(BaseModel):
    category_id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField(default=0)
    category_name = models.CharField(max_length=255, unique=True, null=False, blank=False, db_index=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.category_name


# 定义文章模型
class Article(BaseModel):
    article_id = models.AutoField(primary_key=True)
    article_title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(null=True)

    class Meta:
        db_table = 'article'

    def __str__(self):
        return self.article_title


# 定义视频模型
class Video(BaseModel):
    video_id = models.AutoField(primary_key=True)
    video_title = models.CharField(max_length=255, null=False, blank=False)
    video_description = models.TextField(null=True)
    video_url = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'video'

    def __str__(self):
        return self.video_title


# 定义内容单元模型
class Unit(BaseModel):
    unit_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='units')
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name='units')
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True, related_name='units')
    unit_title = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'unit'

    def __str__(self):
        return self.unit_title
