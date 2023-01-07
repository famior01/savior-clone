from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager



class User(AbstractUser):
    first_name = None
    last_name = None
    
    email = models.EmailField(('email address'), unique=True)
    # username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'religion']

    objects = UserManager()

    def __str__(self):
        return self.username