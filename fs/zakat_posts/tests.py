from django.test import TestCase
from user.models import User
from profiles.models import Profile
from .models import ZakatPosts

# Create your tests here.
class ZakatPostsTestUser(TestCase):
  def setUp(self):
    user = User.objects.create(username='ZakatPosts', password='ZakatPosts', email='ZakatPosts@gamil.com', full_name='ZakatPosts', religion='Muslim')
    profile = Profile.objects.get(user__username='ZakatPosts')
    self.ZakatPosts = ZakatPosts.objects.create(creator=profile)

  def test_profileCreation(self):
    # iwatch=IWatch.objects.get(creator='abuubaida01)
    print("**************", self.ZakatPosts.creator.user.username)
    self.assertEqual(self.ZakatPosts.creator.user.username, 'ZakatPosts')