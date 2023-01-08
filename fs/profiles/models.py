from django.db import models
from django.contrib.auth import get_user_model
from user.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class ProfileManager(models.Manager):
  #TODO: HERE YOU WILL WRITE THE LOGIC OF RECOMMENDATION SYSTEM
  # IT WILL BE DEPENDENT OF MUTUAL following, LOCATION 

  def get_all_profiles(self, me):
    profiles = Profile.objects.all().exclude(user=me)
    return profiles


class Profile(models.Model):
  user                = models.OneToOneField(User, on_delete=models.CASCADE)
  phone_number        = PhoneNumberField(unique=True)
  post_no             = models.IntegerField(default=1)
  intro               = models.TextField(max_length=500, blank=True)
  slogan              = models.CharField(max_length=100, blank=True)
  profession          = models.CharField(max_length=200, blank=True)
  cur_add             = models.CharField(max_length=500, blank=True) 
  avatar              = models.ImageField(default='avatar.jpg', upload_to='avatars/')
  following           = models.ManyToManyField(User, related_name='following', blank=True)
  updated             = models.DateTimeField(auto_now=True)
  created             = models.DateTimeField(auto_now_add=True)

  objects = ProfileManager() # this is the manager
  
  def __str__(self):
    # String representation of the model
    return str(self.user)

  def profile_iwatch(self):
    return self.post_set.all() 
  

  def get_following(self):
    return self.following.all()
  
  def get_following_no(self):
    return self.following.all().count()

  def get_follower_no(self):
    total_user = Profile.objects.filter(following=self.user).count()
    return total_user
  
  def get_followers(self):
    all_users = Profile.objects.filter(following=self.user).all()
    return all_users
  
  # to get the absolute url of the profile
  def get_absolute_url(self):
    return reverse("profiles:profile-detail-view", kwargs={"user": self.user}) 

  def get_post_no(self):
    return self.posts.all().count() 

  def get_all_authors_posts(self):
    return self.posts.all()  

  def get_zakat_posts(self):
    return self.zakat_posts.all()

  def get_zakat_posts_no(self):
    return self.zakat_posts.all().count()
  
  def get_likes_given_no(self):
    """
    like has a relationship with the profile model
    """
    likes = self.like_set.all() # type: ignore
    total_liked = 0
    for item in likes:
      if item.value == 'Like':
          total_liked += 1
    return total_liked

  def get_likes_recieved_no(self):
    posts = self.posts.all() # type: ignore
    total_posts = 0
    for item in posts:
      total_posts+= item.likes.all().count()
    return total_posts
  
  class Meta:
    ordering = ['-created']

  # __initial_first_name = None
  # __initial_last_name = None

  
  # def __init__(self, *args, **kwargs):
  #   super().__init__(*args, **kwargs)
  #   self.__initial_first_name = self.first_name
  #   self.__initial_last_name = self.last_name

  # # to set the slug
  # def save(self, *args, **kwargs):
  #       ex = False
  #       to_slug = self.slug
  #       if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
  #           if self.first_name and self.last_name:
  #               to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
  #               ex = Profile.objects.filter(slug=to_slug).exists()
  #               while ex:
  #                   to_slug = slugify(to_slug + " " + str(get_random_code()))
  #                   ex = Profile.objects.filter(slug=to_slug).exists()
  #           else:
  #               to_slug = str(self.user)
  #       self.slug = to_slug
  #       super().save(*args, **kwargs)

