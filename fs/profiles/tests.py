from django.test import TestCase
from user.models import User
from .models import Profile

# Create your tests here.
class ProfileTestCast(TestCase):
  def setUp(self):
    User.objects.create(username='test', password='test', email='test@gamil.com', full_name='test', religion='Muslim')

  def test_failure(self):
    qs=User.objects.all()
    self.assertEqual(qs.exists(), True)