from django import forms
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ProfileModelForm(forms.ModelForm):
  """
  Here we are going to create a form that will allow us to update our profile
  """
  phone_number = PhoneNumberField(label="Phone Number", widget =PhoneNumberPrefixWidget(initial='PK'))
  slogan = forms.CharField(max_length=80, label='Slogan', required=False, widget=forms.TextInput(attrs={'placeholder': 'People are waiting for your slogan!!'}))
  profession = forms.CharField(max_length=60, label='Profession', required=False, widget=forms.TextInput(attrs={'placeholder': 'Ary you Doctor🤔?'}))
  cur_add = forms.CharField(max_length=100, label='Current Address', required=False, widget=forms.TextInput(attrs={'placeholder': 'ABC(Area), Karachi, Pakistan. By the way, do you live in Mars?'}))
  avatar = forms.ImageField(label='Avatar', required=False)
  intro = forms.CharField(max_length=250, label='Introduction', required=False, widget=forms.Textarea(attrs={'placeholder': 'write your Introduction under 250 letters', 'rows': 2, 'cols': 30}))

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