from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User

from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'city', 'doing', 'about_me',
                  'github_link', 'github_username', 'vk_link', 'inst_username', 'linkedin_link',
                  'facebook_link')


class UserLoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Incorrect login or password")
            return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email address")
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'password2'
        )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            raise forms.ValidationError("This user is registered")
        return super(UserRegisterForm, self).clean(*args, **kwargs)


class ChangePassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Confirm password')


class ProfilesForm(forms.Form):
    names = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'))
