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
        


# class UserChangeForm(forms.ModelForm):
#     password = auth_forms.ReadOnlyPasswordHashField(label="Password",
#         help_text="Raw passwords are not stored, so there is no way to see "
#                 "this user's password, but you can change the password "
#                 "using <a  href=\"account/account_change_password/\" >this form</a>.")

#     class Meta:
#         model = User
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(UserChangeForm, self).__init__(*args, **kwargs)
#         f = self.fields.get('user_permissions', None)
#         if f is not None:
#             f.queryset = f.queryset.select_related('content_type')

#     def clean_password(self):
#         return self.initial["password"]