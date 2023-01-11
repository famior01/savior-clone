from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
from user.models import User
from thumbnails.fields import ImageField


# Create your models here.
class IWatch(models.Model):
  creator       = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='IWatch')
  title         = models.TextField(max_length=100, blank=True, null=True)
  description   = models.TextField(blank=True, null=True)
  thumbnail    = ImageField(upload_to='IWatch/Videos_thumbnails', null=True)
  liked         = models.IntegerField(default=0)
  disliked      = models.IntegerField(default=0)
  created       = models.DateTimeField(auto_now_add=True)
  updated       = models.DateTimeField(auto_now=True)
  
  video         = models.FileField(
                    upload_to='IWatch/Videos',null=True, 
                    validators=[FileExtensionValidator(
                    allowed_extensions=['MOV','avi','mp4','webm','mkv'])
                    ])  
  


  def __str__(self):
    return str(self.creator) + "|" + str(self.title)
  
  def get_num_likes(self):
    return self.likes.all().count()
  
  def get_num_dislikes(self):
    return self.dislikes.all().count()
  
  def get_total_comments(self):
    return self.IWatch_comments.all().count()
  
  def get_all_comments(self):
    return self.IWatch_comments.all()

  # the latest post will be on top
  class Meta:
    ordering = ('-created',)


class IWatchComment(models.Model):
  user    = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='IWatch_users')
  IWatch  = models.ForeignKey(IWatch,  on_delete=models.CASCADE, related_name='IWatch_comments')
  body    = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.pk)
  
  class Meta:
    ordering = ['-created']


class Like(models.Model):
  user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
  IWatch    = models.ForeignKey(IWatch, on_delete=models.CASCADE, related_name='likes')
  liked     = models.BooleanField(default=False)
  created   = models.DateTimeField(auto_now_add=True)
  updated   = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user}-{self.IWatch}"
  
  def get_users(self):
    return self.user.all()


  class Meta:
    ordering = ['-created']

class Dislike(models.Model):
  user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_dislike')
  IWatch    = models.ForeignKey(IWatch, on_delete=models.CASCADE, related_name='dislikes')
  disliked  = models.BooleanField(default=False)
  created   = models.DateTimeField(auto_now_add=True)
  updated   = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user}-{self.IWatch}"

  class Meta:
    ordering = ['-created']

  