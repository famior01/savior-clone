from django.test import TestCase

# Create your tests here.

# create test to check user model

class UserTest(TestCase):
    def setUp(self):
        a_user = User(username='test', full_name='test', email='test01@gmail.com', password='abuubaida')
        a_user.is_staff = True
        a_user.is_superuser = True
        a_user.save()
        print(a_user.id)

    def test_user(self):

        self.assertEqual(self.user.username, 'test')
        self.assertEqual(self.user.full_name, 'test')
        self.assertEqual(self.user.email, 'test01@gmail.com')
