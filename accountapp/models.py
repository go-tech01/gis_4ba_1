from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NewModel(models.Model):
    text = models.CharField(max_length=255, null=False)
    def __str__(self):
        return self.text