from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager



class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    
    email = models.EmailField(_('email address'), unique=True)

    full_name = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email