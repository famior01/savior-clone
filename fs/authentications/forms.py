# https://www.geeksforgeeks.org/python-extending-and-customizing-django-allauth/
# https://django-allauth.readthedocs.io/en/latest/forms.html

from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
  name = forms.CharField(max_length=30, label='Full Name', required=True, widget=forms.TextInput(attrs={'placeholder': 'Like (Abdul Hafeez)'}))
  # last_name = forms.CharField(max_length=30, label='Last Name')

  def save(self, request):
    user = super(CustomSignupForm, self).save(request)
    user.first_name = self.cleaned_data['name']
    # user.last_name = self.cleaned_data['last_name']
    user.save()
    return user