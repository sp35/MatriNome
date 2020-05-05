from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import Profile
from users.models import User


class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','mobile_no', 'image','dob', 'gender','address','state', 'city', 'bio', 'interests']
        widgets = {
            'interests': forms.widgets.CheckboxSelectMultiple,
        }

class AddInterestForm(forms.Form):
    add_interest = forms.CharField(label = 'Other Interests',max_length = 100 ,required = False)


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'input100', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'input100', 'placeholder':'Password'})) 
