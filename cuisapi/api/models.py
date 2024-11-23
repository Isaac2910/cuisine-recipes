from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  
    password = models.CharField(max_length=100)  

    REQUIRED_FIELDS = ['email']  
    def _str_(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True) 
    description = models.TextField()
    ingredients = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title