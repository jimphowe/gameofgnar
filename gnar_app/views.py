from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Climb
from .forms import ClimbForm, SignUpForm

def index(request):
    if request.user.is_authenticated:
        nav = '<a href="/accounts/logout" style="float:right">Log Out</a><a href="/" style="float:right">Logged in as: ' + request.user.username + '</a>'
    else:
        nav = '<a href="/accounts/login" style="float:right">Log In</a><a href="/accounts/signup" style="float:right">Sign Up</a>'
    return render(request, 'index.html', {'account_nav': nav})

def climb_by_id(request, climb_id):
    climb = Climb.objects.get(pk=climb_id)
    return render(request, 'climb_details.html', {'climb':climb})

def dump_climbs(request):
    return render(request, 'dump_climbs.html', {'climb_set': Climb.objects.all().iterator()})

def add_climb(request):
    if request.method == 'POST':
        form = ClimbForm(request.POST, request.FILES)
        if form.is_valid():
            obj = Climb.objects.create(\
            grade = form.cleaned_data.get("grade"),\
            location = form.cleaned_data.get("location"),\
            picture = form.cleaned_data.get("picture"))
            obj.creator = request.user
            obj.save()
            print("VALID")
            return HttpResponseRedirect('/')
        else:
            print("INVALID")
    else:
        form = ClimbForm()
    return render(request, 'add_climb.html', {'form': form})

def trivia_home(request):
    return render(request, 'trivia.html')

def gnar_leaderboard(request):
    return render(request, 'gnar_leaderboard.html')

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
