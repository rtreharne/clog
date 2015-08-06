from django import forms
from invite.models import Invitation

class InviteForm(forms.ModelForm):
    message_text = "Dear Colleague, \n\nI think that you should signup for a CLOGGER account. Then you'll be able to keep track of your cell results and share them with me!"
    message = forms.CharField(widget=forms.Textarea(), initial=message_text)
    class Meta:
        model = Invitation 
        fields = ('email', 'message')
