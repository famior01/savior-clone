from django import forms 
from .models import Like, Comment, Posts
from profiles.models import Profile

class PostModelForm(forms.ModelForm):
    '''
    This form is used to create a post
    '''

    # for changing the size of the text area
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':40}))
    class Meta:
      # will we be changed and these fields will be used
      model = Posts
      fields = ['content', 'image']


class CommentModelForm(forms.ModelForm):
  '''
  This form is used to create a comment
  '''

  # for changing the size of the text area
  body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':"Add a comment...", 'rows':2, 'cols':40}))
  class Meta:
    # will we be changed and these fields will be used
    model = Comment
    fields = ['body']