from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.urls import reverse
# Create your models here.

class ProfileManager(models.Manager):
  '''
  Here we are going to get all the profiles that are not me and are not my friends
  '''
  def get_all_profiles_to_invite(self, sender):
    profiles = Profile.objects.all().exclude(user=sender)
    profile = Profile.objects.get(user=sender)
    qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile)) # Q is a query object which means or
    print(qs)
    accepted = set([])
    for rel in qs:
      if rel.status == 'accepted':
        accepted.add(rel.receiver)
        accepted.add(rel.sender)
    print(accepted)
    available = [profile for profile in profiles if profile not in accepted]
    return available

  #TODO: HERE YOU WILL WRITE THE LOGIC OF RECOMMENDATION SYSTEM
  # IT WILL BE DEPENDENT OF MUTUAL FRIENDS, LOCATION 

  def get_all_profiles(self, me):
    profiles = Profile.objects.all().exclude(user=me)
    return profiles


class Profile(models.Model):
  first_name = models.CharField(max_length=100, blank=True)
  last_name = models.CharField(max_length=100, blank=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE) #if user deleted then profile will be deleted
  post_no = models.IntegerField(default=1)
  bio = models.TextField(default="No bio yet", max_length = 100, blank=True)
  email = models.EmailField(max_length=100, blank=True)
  country = models.CharField(max_length=100, blank=True)
  avatar = models.ImageField(default='avatar.jpg', upload_to='avatars/')
  friends = models.ManyToManyField(User, related_name='friends', blank=True)
  slug = models.SlugField(unique=True, blank=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  objects = ProfileManager() # this is the manager
  
  def __str__(self):
    # String representation of the model
    return str(self.slug)

  # to get the absolute url of the profile
  def get_absolute_url(self):
    return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug}) 

  def get_friends(self):
    return self.friends.all()
  
  def get_friends_no(self):
    return self.friends.all().count()
  
  def get_post_no(self):
    '''
    author has the relationship with the profile model as a name of "posts"
    '''
    return self.posts.all().count() # type: ignore

  def get_all_authors_posts(self):
    return self.posts.all()  # type: ignore

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

  __initial_first_name = None
  __initial_last_name = None

  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__initial_first_name = self.first_name
    self.__initial_last_name = self.last_name

  # to set the slug
  def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)



STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
) # choices for the status of the friend request

class RelationshipManager(models.Manager):
  '''
  here this will handle the friend request
  '''
  def invitations_received(self, receiver):
    qs = Relationship.objects.filter(receiver=receiver, status='send')
    return qs


class Relationship(models.Model):
  """
  Here we need to define the relationship btw users, like who send the request, who received the request and the status of the request.
  """
  sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender') # if the sender is deleted, delete the relationship
  receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver') # if the receiver is deleted, delete the relationship
  status = models.CharField(max_length=8, choices=STATUS_CHOICES)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  objects = RelationshipManager() # this is the manager


  def __str__(self):
    return f'{self.sender}-{self.receiver}-{self.status}'
    