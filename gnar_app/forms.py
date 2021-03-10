from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import GYMS, SCHOOLS, GENERAL_POINTS, WORKOUTS, MEETINGS, Climb, GeneralPoints, MeetingAttended, WorkoutAttended, Comment, AddOnGame, AddOnEntry


class ClimbForm(forms.ModelForm):
    grade = forms.IntegerField()
    location = forms.ChoiceField(choices=GYMS)
    picture = forms.ImageField()
    
    class Meta:
        model = Climb
        fields = ('grade', 'location', 'picture')

class GeneralPointsForm(forms.ModelForm):
    kind = forms.ChoiceField(choices=GENERAL_POINTS)
    location = forms.ChoiceField(choices=GYMS)

    class Meta:
        model = GeneralPoints
        fields = ('kind', 'location')
    
class MeetingAttendanceForm(forms.ModelForm):
    date = forms.ChoiceField(choices=MEETINGS)

    class Meta:
        model = MeetingAttended
        fields = ('date',)


class WorkoutAttendanceForm(forms.ModelForm):
    date = forms.ChoiceField(choices=WORKOUTS)

    class Meta:
        model = WorkoutAttended
        fields = ('date',)

class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=300, required=True, help_text='Max 300 chars.')

    class Meta:
        model = Comment
        fields = ('comment',)

class AddOnGameForm(forms.ModelForm):
    grade = forms.IntegerField()
    location = forms.ChoiceField(choices=GYMS)

    class Meta:
        model = AddOnGame
        fields = ('grade', 'location',)

class AddOnEntryForm(forms.ModelForm):
    picture = forms.ImageField()

    class Meta:
        model = AddOnEntry
        fields = ('picture',)

class FilterForm(forms.ModelForm):
    gym = forms.ChoiceField(choices=GYMS)
    class Meta:
        model = Climb
        fields = ('gym',)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid @northeastern.edu email address.')
    school = forms.ChoiceField(choices=SCHOOLS)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'school',)

