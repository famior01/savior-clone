from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):
  """
  Here we are going to create a form that will allow us to update our profile
  """
  class Meta:
    model = Profile
    fields = [
      'first_name',
      'last_name',
      'avatar',
      'bio',
    ]