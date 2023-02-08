from django.test import TestCase
from user.models import User
from .models import Profile

# Create your tests here.
class ProfileTestCast(TestCase):
  def setUp(self):
    User.objects.create(username='Profile', password='Profile', email='Profile@gamil.com', full_name='Profile', religion='Muslim')

  def test_profileCreation(self):
    profile=Profile.objects.get(user__username='Profile')
    print("**************", profile.user.username)
    self.assertEqual(profile.user.username, 'Profile')