from django import forms 
from .models import ZakatPosts, ZakatPostsComment

class ZakatPostForm(forms.ModelForm):
    '''
    This form is used to create and update a post
    '''
    # for changing the size of the text area
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':40}))
    class Meta:
      # will we be changed and these fields will be used
      model = ZakatPosts
      fields = ['seeker', 'expected_money', 'video1', 'video2', 'content']


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