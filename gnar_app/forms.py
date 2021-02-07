from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import GYMS, Climb


class ClimbForm(forms.ModelForm):
    grade = forms.IntegerField()
    location = forms.ChoiceField(choices=GYMS)
    picture = forms.ImageField()
    
    class Meta:
        model = Climb
        fields = ('grade', 'location', 'picture')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid @northeastern.edu email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

