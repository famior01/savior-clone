from django import forms
from .models import SaviorMembers

class SaviorMembersForm(forms.ModelForm):
    class Meta:
        model = SaviorMembers
        fields = ('member_profile', 'deposit_receipt')