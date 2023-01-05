from django import forms 
from .models import ZakatPosts, ZakatPostsComment

class ZakatPostForm(forms.ModelForm):
    '''
    This form is used to create and update a post
    '''
    # for changing the widget of the fields
    seeker = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Seeker Name (Fajar..)", 'type': 'text', 'required': 'required', 'label':''}))
    needed_money = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"How much do you need (10,000)", 'type': 'number', 'required': 'required'}))
    video1 = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'accept': 'video/*' , 'style': 'width: 200px;', 'required': 'required'}))
    video2 = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'accept': 'video/*' , 'style': 'width: 200px;', 'required': 'required'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write something (optional)", 'rows':1, 'cols':40, }))
    
    class Meta:
      # will we be changed and these fields will be used
      model = ZakatPosts
      fields = ['seeker', 'needed_money', 'video1', 'video2', 'content']
    
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['content'].label = ''
      self.fields['seeker'].label = ''
      self.fields['needed_money'].label = ''
      self.fields['video1'].label = ''
      self.fields['video2'].label = ''
      self.fields['content'].required = False


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