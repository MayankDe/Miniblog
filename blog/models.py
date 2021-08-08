from django.contrib.auth.forms import PasswordResetForm
from django.db import models
from django.db.models.base import Model

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=150)
    desc=models.TextField()
    
    def __str__(self):
        return self.title