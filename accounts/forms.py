from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                               min_length=8,
                               label="Password"
                               )
    first_name = forms.CharField(label="First name",
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label="Last name",
                                 required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(label="Username",
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password"]


class AuthenticationForm(forms.Form):

    username = forms.CharField(label='Username',
                        widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'shit'}),
        min_length=8, label="Password")

    error_messages = {
        'invalid_login': "Invalid login credentials"
    }

    def __init__(self, request = None, *args, **kwargs):

        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AuthenticationForm, self).clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:

            self.user_cache = authenticate(self.request, username=username,password=password)

            if self.user_cache  is None:

                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login'
                )

        return cleaned_data

    def get_user(self):
        return self.user_cache