from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div,Row,Column,Field

# Create your forms here.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
        'username':forms.TextInput(attrs={'id':'nameid','placeholder':'Username'}),
        'email':forms.EmailInput(attrs={'id':'emailid','placeholder':'Email'}),
        'password':forms.PasswordInput(attrs={'id':'passwordid','placeholder':'Password'}),
        } 




    
