from django.contrib import admin

# Register your models here.
from commentapp.models import Comment

admin.site.register(Comment)
