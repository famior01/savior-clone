from django.db import models
from user.models import User
from IWatch.models import IWatch
from profiles.models import Profile
from zakat_posts.models import ZakatPost
# Create your models here.

# uncommit from dockerignore! TODO;

class Sugg2Savior(models.Model):
  profile             = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile')
  suggestion          = models.TextField(max_length=500, blank=True)
  updated             = models.DateTimeField(auto_now=True)
  created             = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.profile)


class ReportSaviorProblem(models.Model):
  profile             = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile')
  # savior_problem      = models.ForeignKey(SaviorProblem, on_delete=models.CASCADE, related_name='savior_problem')
  report              = models.TextField(max_length=500, blank=True)
  updated             = models.DateTimeField(auto_now=True)
  created             = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.profile)


class ReportZakatPost(models.Model):
  profile             = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile')
  zakat_post          = models.ForeignKey(ZakatPost, on_delete=models.CASCADE, related_name='zakat_post')
  report              = models.TextField(max_length=500, blank=True)
  updated             = models.DateTimeField(auto_now=True)
  created             = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.profile)

class ReportIWatch(models.Model):
  profile             = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile')
  iwatch              = models.ForeignKey(IWatch, on_delete=models.CASCADE, related_name='iwatch')
  report              = models.TextField(max_length=500, blank=True)
  updated             = models.DateTimeField(auto_now=True)
  created             = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.profile)

