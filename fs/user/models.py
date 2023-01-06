from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    religion = {
        ('Muslim', 'Muslim'),
        ('Christian', 'Christian'),
        ('Hindu', 'Hindu'),
        ('Buddhist', 'Buddhist'),
        ('Jewish', 'Jewish'),
        ('Sikh', 'Sikh'),
        ('Atheist', 'Atheist'),
        ('Agnostic', 'Agnostic'),
        ('Other', 'Other'),
    }
    religion = models.CharField(max_length=100, choices=religion)

    def __str__(self):
        return self.full_name
        
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    