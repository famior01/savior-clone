from django.db import models
from user.models import User
from IWatch.models import IWatch
from profiles.models import Profile
from zakat_posts.models import ZakatPosts
# Create your models here.

# uncommit from dockerignore! TODO;

class Sugg2Savior(models.Model):
  savior_adviser      = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='savior_adviser')
  suggestion          = models.TextField(max_length=1000, blank=True)
  created             = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.savior_adviser)


class ReportSaviorProblem(models.Model):
  savior_reporter     = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='savior_reporter')
  problem             = models.TextField(max_length=1000, blank=True)
  created             = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.savior_reporter)


class ReportZakatPost(models.Model):
  zakat_reporter         = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='zakat_reporter')
  reported_zp            = models.ForeignKey(ZakatPosts, on_delete=models.CASCADE, related_name='reported_zp')
  problem                = models.TextField(max_length=500, blank=True)
  created                = models.DateTimeField(auto_now_add=True)

  
  def __str__(self):
    return str(self.zakat_reporter) +"|"+ str(self.reported_zp)

class ReportIWatch(models.Model):
  iwatch_reporter     = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='iwatch_reporter')
  reported_iw         = models.ForeignKey(IWatch, on_delete=models.CASCADE, related_name='reported_iw')
  problem             = models.TextField(max_length=500, blank=True)
  created             = models.DateTimeField(auto_now_add=True)

  
  def __str__(self):
    return str(self.iwatch_reporter) +"|"+ str(self.reported_iw)


class ReportUser(models.Model):
  reporter_profile     = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reporter_profile')
  reported_profile     = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reported_profile')
  problem           = models.TextField(max_length=500, blank=True)
  created           = models.DateTimeField(auto_now_add=True)

  
  def __str__(self):
    return str(self.reporter_profile) +"|"+ str(self.reported_profile)


