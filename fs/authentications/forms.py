# https://www.geeksforgeeks.org/python-extending-and-customizing-django-allauth/
# https://django-allauth.readthedocs.io/en/latest/forms.html

from allauth.account.forms import SignupForm
from django import forms
from allauth.account.forms import AddEmailForm


religion = [
        ('Muslim', 'Muslim'),
        ('Hindu', 'Hindu'),
        ('Christian', 'Christian'),
        ('Sikh', 'Sikh'),
        ('Buddhist', 'Buddhist'),
        ('Jewish', 'Jewish'),
        ('Atheist', 'Atheist'),
        ('Agnostic', 'Agnostic'),
        ('Other', 'Other'),
    ]

gender = [
  ('Male','Male'),
  ('Female', 'Female'),
  ('Transgender', 'Transgender'),

]

class CustomSignupForm(SignupForm):
  name = forms.CharField(max_length=30, label='Full Name', required=True, widget=forms.TextInput(attrs={'placeholder': 'Like (Abdul Hafeez)'}))

  religion = forms.CharField(max_length=30, label='Religion', required=True, widget=forms.Select(choices=religion, attrs={'placeholder': 'Select your religion'}))

  gender = forms.CharField(max_length=30, label='Religion', required=True, widget=forms.Select(choices=gender,  attrs={'placeholder': 'Select your Gender'}))


  
  def save(self, request):
    user = super(CustomSignupForm, self).save(request)
    user.full_name = self.cleaned_data['name']
    user.religion = self.cleaned_data['religion']
    user.gender = self.cleaned_data['gender']

    user.save()
    return user