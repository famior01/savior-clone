from django import forms
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ProfileModelForm(forms.ModelForm):
  """
  Here we are going to create a form that will allow us to update our profile
  """
  phone_number = PhoneNumberField(label="Phone Number", widget =PhoneNumberPrefixWidget(initial='PK'))
  slogan = forms.CharField(max_length=100, label='Slogan', required=False, widget=forms.TextInput(attrs={'placeholder': 'Like (I am a programmer)'}))
  profession = forms.CharField(max_length=100, label='Profession', required=False, widget=forms.TextInput(attrs={'placeholder': 'Like (Software Engineer)'}))
  cur_add = forms.CharField(max_length=500, label='Current Address', required=False, widget=forms.TextInput(attrs={'placeholder': 'Like (Karachi, Pakistan)'}))
  avatar = forms.ImageField(label='Avatar', required=False)
  intro = forms.CharField(max_length=500, label='Introduction', required=False, widget=forms.Textarea(attrs={'placeholder': 'I am a software engineer and I am working in a company', 'rows': 3, 'cols': 30}))

  class Meta:
    model = Profile
    fields = [
      'phone_number',
      'slogan',
      'profession',
      'cur_add',
      'avatar',
      'intro'
    ]