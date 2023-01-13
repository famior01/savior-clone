from django import forms 
from .models import Like, IWatchComment, IWatch 
from profiles.models import Profile

class IWatchModelForm(forms.ModelForm):
    
    '''
    This form is used to create and update a post
    '''
    # for changing the widget of the fields
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title of your Video (under 100 letters)", 'type': 'text', 'row':1, 'cols':40}))

    video = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'accept': 'video/*' , 'style': 'width: 200px;'}))

    thumbnail = forms.ImageField()

    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write description upto", 'rows':3, 'cols':40 }))
    
    class Meta:
      # will we be changed and these fields will be used
      model = IWatch
      fields = ['title', 'video', 'thumbnail', 'description']
    
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['title'].required = True 
      self.fields['video'].required = True
      self.fields['thumbnail'].required= False
      self.fields['description'].required = False


      # some css class like field
      for i,field in enumerate(self.fields):
        self.fields[str(field)].widget.attrs['class'] = 'field'+str(i+1)
        # id to each field
        self.fields[str(field)].widget.attrs['id'] = 'field'+str(i+1)



class CommentModelForm(forms.ModelForm):
  '''
  This form is used to create a comment
  '''

  # for changing the size of the text area
  body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':"Add a comment...", 'rows':2, 'cols':40}))
  class Meta:
    # will we be changed and these fields will be used
    model = IWatchComment
    fields = ['body']