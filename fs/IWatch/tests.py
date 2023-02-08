from django.test import TestCase
from user.models import User
from profiles.models import Profile
from .models import IWatch

# Create your tests here.
class IWatchTestCast(TestCase):
  def setUp(self):
    user = User.objects.create(username='IWatch', password='IWatch', email='IWatch@gamil.com', full_name='IWatch', religion='Muslim')
    profile = Profile.objects.get(user__username='IWatch')
    self.iwatch = IWatch.objects.create(creator=profile)

  def test_profileCreation(self):
    # iwatch=IWatch.objects.get(creator='abuubaida01)
    print("**************", self.iwatch.creator.user.username)
    self.assertEqual(self.iwatch.creator.user.username, 'IWatch')