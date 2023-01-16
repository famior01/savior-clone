from django import forms
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ProfileModelForm(forms.ModelForm):
  """
  Here we are going to create a form that will allow us to update our profile
  """
  phone_number = PhoneNumberField(label="Phone Number", widget =PhoneNumberPrefixWidget(initial='PK'))
  slogan = forms.CharField(max_length=80, label='Slogan', required=False, widget=forms.TextInput(attrs={'placeholder': 'People are waiting for your slogan or any favorite line.'}))
  profession = forms.CharField(max_length=60, label='Profession', required=False, widget=forms.TextInput(attrs={'placeholder': 'Ary you Doctor🤔?'}))
  cur_add = forms.CharField(max_length=100, label='Current Address', required=False, widget=forms.TextInput(attrs={'placeholder': 'ABC(Area), Karachi, Pakistan. By the way, do you live on Mars?'}))
  picture = forms.ImageField(widget=forms.FileInput(attrs={'type': 'file', 'accept': 'image/*' , 'style': 'width: 20em; height: 50px;'}))
  intro = forms.CharField(max_length=250, label='Introduction', required=False, widget=forms.Textarea(attrs={'placeholder': 'write your Introduction under 250 letters', 'rows': 2, 'cols': 30}))
  bank_details = forms.CharField(max_length=500, label='Bank Details', required=False, widget=forms.Textarea(attrs={'placeholder': 'Give your Bank details, if you want to create video content', 'rows': 1, 'cols': 30}))

  class Meta:
    model = Profile
    fields = [
      'slogan',
      'intro',
      'phone_number',
      'profession',
      'cur_add',
      'bank_details',
      'picture',
    ]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['phone_number'].required = False
    self.fields['slogan'].required = False
    self.fields['profession'].required = False
    self.fields['cur_add'].required = False
    self.fields['picture'].required = False
    self.fields['intro'].required = False
    self.fields['bank_details'].required = False
      
    # some css class like field
    for i,field in enumerate(self.fields):
      self.fields[str(field)].widget.attrs['class'] = 'field'+str(i+1)
      # id to each field
      self.fields[str(field)].widget.attrs['id'] = 'field'+str(i+1)
  