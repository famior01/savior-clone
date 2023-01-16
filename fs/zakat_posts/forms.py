from django import forms 
from .models import ZakatPosts, ZakatPostsComment
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class ZakatPostForm(forms.ModelForm):
    '''
    This form is used to create and update a post
    '''
    # for changing the widget of the fields
    seeker = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Seeker Name (Fajar..)", 'type': 'text', 'required': 'required'}))
    needed_money = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"How much do you need (10,000)", 'type': 'number', 'required': 'required'}))
    video1 = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'accept': 'video/*' , 'style': 'width: 200px;', 'required': 'required'}))
    video2 = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'accept': 'video/*' , 'style': 'width: 200px;', 'required': 'required'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write something (optional)", 'rows':1, 'cols':40, 'label':'' }))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Address (House, Street, Area, City, Country)", 'rows':1, 'cols':40 }))
    phone_number = PhoneNumberField(label="Phone Number", widget =PhoneNumberPrefixWidget(initial='PK'))
    bank_details = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Bank Details (Bank Name, Account Number, Account Title)", 'rows':1, 'cols':40,'required': 'required' }))

    class Meta:
      # will we be changed and these fields will be used
      model = ZakatPosts
      fields = ['seeker','phone_number','address', 'needed_money', 'video1', 'video2','bank_details' ,'content']
    
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['seeker'].label = ''
      self.fields['needed_money'].label = ''
      self.fields['address'].label = ''
      self.fields['phone_number'].label = ''
      self.fields['video1'].label = 'Video 1'
      self.fields['video2'].label = 'Video 2'
      self.fields['content'].required = False
      self.fields['content'].label = '' 
      self.fields['bank_details'].label = ''


      # some css class like field
      for i,field in enumerate(self.fields):
        self.fields[str(field)].widget.attrs['class'] = 'field'+str(i+1)
        # id to each field
        self.fields[str(field)].widget.attrs['id'] = 'field'+str(i+1)
    
    


class ZakatPostsCommentForm(forms.ModelForm):
  '''
  This form is used to create  a comment
  '''

  # for changing the size of the text area
  body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':"Add a comment...", 'rows':1, 'cols':40, 'id':'commentbody'}))
  class Meta:
    # will we be changed and these fields will be used
    model = ZakatPostsComment
    fields = ['body']