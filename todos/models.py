from django.db import models
from datetime import datetime
from django.conf import settings
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Todo(models.Model):
    title=models.CharField(max_length=200)
    text=models.TextField()
    created_at=models.DateTimeField(default=datetime.now,blank=True)
    description = models.TextField(null=False)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='todos')
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='todos')
    def __str__(self):
        return self.title
