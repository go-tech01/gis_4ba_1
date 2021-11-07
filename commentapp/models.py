from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from articleapp.models import Article


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, related_name='comment',null=True)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comment',null=True)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.article} - {self.writer} --- {self.created_at}'