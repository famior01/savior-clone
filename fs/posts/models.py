from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile

# Create your models here.
class Posts(models.Model):
  
  content = models.TextField()
  image = models.ImageField(upload_to='posts/images', blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])
  liked = models.ManyToManyField(Profile, blank=True, related_name='likes') # track the profliel who liked the post, related_name works when there is reverse relationship
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts') # track the profile who created the post as a foreign key to the profile model

  def __str__(self):
    return self.content + ' | ' + str(self.author)
  
  def num_likes(self):
    return self.liked.all().count()
  
  def num_comments(self):
        return self.comment_set.all().count() # type: ignore 
  
  # the latest post will be on top
  class Meta:
    ordering = ('-created_at',)


class Comment(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  post = models.ForeignKey(Posts,  on_delete=models.CASCADE)
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.pk)
  
  class Meta:
    ordering = ['-created_at']


LIKE_CHOICES = (
    ('Like', 'Like'), 
    ('Unlike', 'Unlike'), 
)
class Like(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  post = models.ForeignKey(Posts, on_delete=models.CASCADE, 
  related_name='likes')
  value = models.CharField(choices = LIKE_CHOICES, max_length=8)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user}-{self.post}-{self.value}"

  class Meta:
    ordering = ['-created_at']