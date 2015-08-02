from django import forms
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Pass')
    password2.help_text = None
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)

    class Meta:
        model = User
    	fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email address has already been registered')
        return email

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['picture'].label = 'Picture'

    class Meta:
        model = UserProfile
        fields = ('affiliation', 'picture', 'bio', 'url', 'linkedin', 'twitter')

