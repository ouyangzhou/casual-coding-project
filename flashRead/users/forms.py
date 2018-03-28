from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from users.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.validator import validate_email_unique

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email_unique])
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        myuser = super(UserCreateForm, self).save(commit=False)
        myuser.email = self.cleaned_data["email"]
        if commit:
            myuser.save()
        return myuser
     
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about', 'gender')
        
    def __str__(self):
     return (self.myuser)
        
