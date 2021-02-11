from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Climb
from .forms import ClimbForm, SignUpForm


b_log_out = '<a href="/accounts/logout" style="float:right">Log Out</a>'
b_logged_in_as = lambda request : ('<a href="/" style="float:right">Logged in as: ' + request.user.username + '</a>')
b_add_climb = '<a href="/add_climb" style="float:right">Add Climb</a>'
ba_add_climb = '<a class="active" href="/add_climb" style="float:right">Add Climb</a>'
b_view_climbs = '<a href="/view_climbs" style="float:right">View Climbs</a>'
ba_view_climbs = '<a class="active" href="/view_climbs" style="float:right">View Climbs</a>'
b_view_leaderboard = '<a href="/gnar_leaderboard" style="float:right">View Leaderboard</a>'
ba_view_leaderboard = '<a class="active" href="/gnar_leaderboard" style="float:right">View Leaderboard</a>'

b_log_in = '<a href="/accounts/login" style="float:right">Log In</a>'
b_sign_up = '<a href="/accounts/signup" style="float:right">Sign Up</a>'




def index(request):
    if request.user.is_authenticated:
        nav = b_log_out + b_logged_in_as(request) + b_add_climb + b_view_climbs + b_view_leaderboard
    else:
        nav = b_log_in + b_sign_up
    return render(request, 'index.html', {'account_nav': nav})

def climb_by_id(request, climb_id):
    climb = Climb.objects.get(pk=climb_id)
    return render(request, 'climb_details.html', {'climb':climb})

def view_climbs(request):
    nav = b_log_out + b_logged_in_as(request) + b_add_climb + ba_view_climbs + b_view_leaderboard
    return render(request, 'view_climbs.html', {'climb_set': Climb.objects.all().iterator(), 'account_nav': nav})

def add_climb(request):
    if request.method == 'POST':
        form = ClimbForm(request.POST, request.FILES)
        if form.is_valid():
            obj = Climb.objects.create(\
            grade = form.cleaned_data.get("grade"),\
            location = form.cleaned_data.get("location"),\
            picture = form.cleaned_data.get("picture"))
            obj.creator = str(request.user)
            obj.save()
            print("VALID")
            return HttpResponseRedirect('/')
        else:
            print("INVALID")
    else:
        form = ClimbForm()
    nav = b_log_out + b_logged_in_as(request) + ba_add_climb + b_view_climbs + b_view_leaderboard
    return render(request, 'add_climb.html', {'form': form, 'account_nav': nav})


def trivia_home(request):
    return render(request, 'trivia.html')

def gnar_leaderboard(request):
    nav = b_log_out + b_logged_in_as(request) + b_add_climb + b_view_climbs + ba_view_leaderboard
    return render(request, 'gnar_leaderboard.html', {'account_nav': nav})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def loggedincheck(request):
    if request.user.is_authenticated:
        return render(request, 'loggedincheck.html', {'username':request.user.username, 'email':request.user.email})
    else:
        return render(request, 'loggedincheck.html', {'username':"NOT LOGGED IN", 'email':''})
