from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User
from django.contrib.auth import forms as auth_forms
from django import forms




class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)



class UserChangeForm(auth_forms.UserChangeForm):
    password = auth_forms.ReadOnlyPasswordHashField(label="Password")
    class Meta:
        model = User
        fields = ['full_name','username'] 
        