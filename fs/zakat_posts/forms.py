from django import forms 
from .models import ZakatPosts, ZakatPostsComment

class ZakatPostForm(forms.ModelForm):
    '''
    This form is used to create and update a post
    '''
    # for changing the widget of the fields
    seeker = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"like Asar", 'style': 'width: 200px;', 'type': 'text', 'required': 'required'}))
    needed_money = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"like 10,000", 'type': 'number', 'style': 'width: 200px;', 'required': 'required'}))
    video1 = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'accept': 'video/*' , 'style': 'width: 200px;', 'required': 'required'}))
    video2 = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'accept': 'video/*' , 'style': 'width: 200px;', 'required': 'required'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"you can write anything that you have missed in the video, remember it is optional", 'rows':1, 'cols':40, }))
    
    class Meta:
      # will we be changed and these fields will be used
      model = ZakatPosts
      fields = ['seeker', 'needed_money', 'video1', 'video2', 'content']
    
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['content'].label = 'Extra Information*'
      self.fields['seeker'].label = 'Seeker Name*'
      self.fields['needed_money'].label = 'needed Money*'
      self.fields['video1'].label = 'First Video*'
      self.fields['video2'].label = 'Second Video*'
      self.fields['content'].required = False


      # some css class like field
      for i,field in enumerate(self.fields):
        self.fields[str(field)].widget.attrs['class'] = 'field'+str(i+1)
    
    


class ZakatPostsCommentForm(forms.ModelForm):
  '''
  This form is used to create  a comment
  '''

  # for changing the size of the text area
  body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':"Add a comment...", 'rows':1, 'cols':40}))
  class Meta:
    # will we be changed and these fields will be used
    model = ZakatPostsComment
    fields = ['body']