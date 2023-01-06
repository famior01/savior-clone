from django import forms
from user.models import User

class UserForm(forms.modelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'religion']
    