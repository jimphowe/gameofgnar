from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Climb, GeneralPoints, MeetingAttended, WorkoutAttended, GENERAL_POINTS, MEETINGS, WORKOUTS, ClimbComplete, MiscellaneousPoints, Comment, ResetReport, AddOnGame, AddOnEntry
from .forms import ClimbForm, SignUpForm, GeneralPointsForm, MeetingAttendanceForm, WorkoutAttendanceForm, CommentForm, AddOnGameForm, AddOnEntryForm, FilterForm

##########################
# NAVIGATION DEFINITIONS #
##########################
b_log_out = '<a href="/accounts/logout" style="float:right">Log Out</a>'
b_logged_in_as = lambda request : ('<a href="/profile" style="float:right"><img src="/static/images/profile.png" style="width:16px; height: 16px"> ' + request.user.username + '</a>')
ba_logged_in_as = lambda request : ('<a class="active" href="/profile" style="float:right"><img src="/static/images/profile.png" style="width:16px; height: 16px"> ' + request.user.username + '</a>')
b_add_climb = '<a href="/add_climb" style="float:right">Add Climb</a>'
ba_add_climb = '<a class="active" href="/add_climb" style="float:right">Add Climb</a>'
b_view_climbs = '<a href="/view_climbs" style="float:right">View Climbs</a>'
ba_view_climbs = '<a class="active" href="/view_climbs" style="float:right">View Climbs</a>'
b_view_leaderboard = '<a href="/gnar_leaderboard" style="float:right">View Leaderboard</a>'
ba_view_leaderboard = '<a class="active" href="/gnar_leaderboard" style="float:right">View Leaderboard</a>'

b_log_in = '<a href="/accounts/login" style="float:right">Log In</a>'
b_sign_up = '<a href="/accounts/signup" style="float:right">Sign Up</a>'

####################
# Helper Functions #
####################
def redirect_if_not_logged_in(request, callback):
    if request.user.is_authenticated:
        return callback(request)
    else:
        return redirect('/')

def completed_climb(climb_id, user):
    for completion in ClimbComplete.objects.all().iterator():
        if completion.user == str(user) and completion.climb_id == climb_id:
            return True
    return False

def complained_climb(climb_id, user):
    for completion in ResetReport.objects.all().iterator():
        if completion.user == str(user) and completion.climb_id == climb_id and completion.is_climb_complaint:
            return True
    return False

def complained_add_on(game_id, user):
    for completion in ResetReport.objects.all().iterator():
        if completion.user == str(user) and completion.climb_id == game_id and not completion.is_climb_complaint:
            return True
    return False

def annotate_completion(climb, user):
    climb_id = climb.id
    climb.completed = completed_climb(climb_id, user)
    sends = 0
    for completion in ClimbComplete.objects.all().iterator():
        if completion.climb_id == climb_id:
            sends += 1
    climb.sends = sends
    climb.plural_sends = False if sends == 1 else True
    """
    comments = 0
    for comment in Comment.objects.all().iterator():
        if comment.climb_id == climb_id:
            comments += 1
    climb.comments = comments
    """


# NOTE: This is about whether a climb has been completed by anybody except its creator
def climb_has_been_completed(climb_id, user):
    for completion in ClimbComplete.objects.all().iterator():
        if completion.user != str(user) and completion.climb_id == climb_id:
            return True
    return False

# None -> {user -> [(points, description, time)]}
def get_point_history():
    points = {}
    def add_key(user, value):
        if user in points:
            points[user] = points[user] + [value]
        else:
            points[user] = [value]
    # Number -> String -> String -> Value
    def pack(points, type_, date):
        return {"date":date, "points": points, "type": type_}
    def points_of_kind(kind):
        mapping = {1:250, 2:500, 3:250}
        return mapping[kind]
    def content_of_enum(val, enum):
        for (i, s) in enum:
            if i == val:
                return s
    for climb in Climb.objects.all().iterator():
        point_value = 0 if not climb_has_been_completed(climb.id, climb.creator) else 250
        add_key(climb.creator, pack(point_value, "Custom Climb", str(climb.time_added.date().isoformat())))
    for m_p in MiscellaneousPoints.objects.all().iterator():
        add_key(m_p.user, pack(m_p.points, m_p.description, str(m_p.time_added.date().isoformat())))
    for g_p in GeneralPoints.objects.all().iterator():
        add_key(g_p.user, pack(points_of_kind(g_p.kind), content_of_enum(g_p.kind, GENERAL_POINTS), str(g_p.time_added.date().isoformat())))
    for meeting in MeetingAttended.objects.all().iterator():
        add_key(meeting.user, pack(100, "Meeting Attended", content_of_enum(meeting.date, MEETINGS)))
    for workout in WorkoutAttended.objects.all().iterator():
        add_key(workout.user, pack(100, "Workout Attended", content_of_enum(workout.date, WORKOUTS)))
    for completion in ClimbComplete.objects.all().iterator():
        climb = Climb.objects.get(pk=completion.climb_id)
        if climb.creator != completion.user:
            add_key(completion.user, pack(100, "<a href='../climbs/" + str(completion.climb_id) + "'>Completed Climb " + str(completion.climb_id) + "</a>", str(completion.time_added.date().isoformat())))
    return points

# None -> [(user, points)]
def get_user_point_map():
    umap = []
    for (k, v) in get_point_history().items():
        total = 0
        for e in v:
            total += e["points"]
        umap += [{"user":k, "points":total}]
    umap = sorted(umap, reverse=True, key=(lambda item: item["points"]))
    return umap


#############
# HOME PAGE #
#############
def index(request):
    if request.user.is_authenticated:
        nav = b_log_out + b_logged_in_as(request) + b_add_climb + b_view_climbs + b_view_leaderboard
    else:
        nav = b_log_in + b_sign_up
    return render(request, 'index.html', {'account_nav': nav})

####################
# LOGGED OUT PAGES #
####################
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

###################
# LOGGED IN PAGES #
###################
def view_climbs(request):
    def callback(request):
        nav = b_log_out + b_logged_in_as(request) + b_add_climb + ba_view_climbs + b_view_leaderboard
        climb_set = []
        re_set = []
        for climb in Climb.objects.all().iterator():
            annotate_completion(climb, request.user)
            if climb.reset:
                re_set.append(climb)
            else:
                climb_set.append(climb)
        adds_on = []
        for game in AddOnGame.objects.all().iterator():
            user_set = set()
            moves = 0
            for entry in AddOnEntry.objects.all().iterator():
                if entry.add_on_game == game.id:
                    user_set.add(entry.creator)
                    moves += 1
            game.participants = len(user_set)
            game.plural_parts = False if game.participants == 1 else True
            game.moves = moves
            game.plural_moves = False if moves == 1 else True
            adds_on.append(game)
        form = FilterForm()
        if request.method == 'POST':
            if 'filter_now' in request.POST:
                form = FilterForm(request.POST)
                if form.is_valid():
                    location_matches = lambda obj: obj.location == form.cleaned_data.get("gym")
                    re_set = list(filter(location_matches, re_set))
                    climb_set = list(filter(location_matches, climb_set))
                    adds_on = list(filter(location_matches, adds_on))
        return render(request, 'view_climbs.html', {'re_set': re_set,'climb_set': climb_set, 'account_nav': nav, 'adds_on':adds_on, 'form':form})
    return redirect_if_not_logged_in(request, callback)

def add_climb(request):
    def callback(request):
        form = ClimbForm()
        add_on_form = AddOnGameForm()
        if request.method == 'POST':
            if 'new_climb' in request.POST: 
                form = ClimbForm(request.POST, request.FILES)
                if form.is_valid():
                    obj = Climb.objects.create(\
                    grade = form.cleaned_data.get("grade"),\
                    location = form.cleaned_data.get("location"),\
                    picture = form.cleaned_data.get("picture"))
                    obj.creator = str(request.user)
                    obj.save()
                    return HttpResponseRedirect('/')
            elif 'add_on' in request.POST:
                add_on_form = AddOnGameForm(request.POST)
                if add_on_form.is_valid():
                    obj = AddOnGame.objects.create(\
                    grade = add_on_form.cleaned_data.get("grade"),\
                    location = add_on_form.cleaned_data.get("location"))
                    obj.creator = str(request.user)
                    obj.save()
                    return HttpResponseRedirect('/')
        nav = b_log_out + b_logged_in_as(request) + ba_add_climb + b_view_climbs + b_view_leaderboard
        return render(request, 'add_climb.html', {'form': form, 'account_nav': nav, 'add_on_form':add_on_form})
    return redirect_if_not_logged_in(request, callback)

def gnar_leaderboard(request):
    def callback(request):
        nav = b_log_out + b_logged_in_as(request) + b_add_climb + b_view_climbs + ba_view_leaderboard
        user_point_map = [] 
        for e in get_user_point_map():
            if e['user'] != "admin":
                user_point_map.append(e)
        return render(request, 'gnar_leaderboard.html', {'account_nav': nav, 'user_point_map':user_point_map})
    return redirect_if_not_logged_in(request, callback)

def profile(request):
    def callback(request):
        general_form = GeneralPointsForm()
        meeting_form = MeetingAttendanceForm()
        workout_form = WorkoutAttendanceForm()
        if request.method == 'POST':
            if 'general_points' in request.POST:
                general_form = GeneralPointsForm(request.POST)
                if general_form.is_valid():
                    obj = general_form.save(commit=False)
                    obj.user = str(request.user)
                    obj.save()
                    return HttpResponseRedirect('/profile')
            elif 'meeting' in request.POST:
                meeting_form = MeetingAttendanceForm(request.POST)
                if meeting_form.is_valid():
                    obj = MeetingAttended.objects.create(\
                    date = meeting_form.cleaned_data.get("date"))
                    obj.user = str(request.user)
                    obj.save()
                    return HttpResponseRedirect('/profile')
            elif 'workout' in request.POST:
                workout_form = WorkoutAttendanceForm(request.POST)
                if workout_form.is_valid():
                    obj = WorkoutAttended.objects.create(\
                    date = workout_form.cleaned_data.get("date"))
                    obj.user = str(request.user)
                    obj.save()
        nav = b_log_out + ba_logged_in_as(request) + b_add_climb + b_view_climbs + b_view_leaderboard
        point_hist = get_point_history()
        if str(request.user) in point_hist:
            point_hist = point_hist[str(request.user)]
        else:
            point_hist = []
        points = 0
        for i in point_hist:
            points += i["points"]
        return render(request, 'account.html', {'account_nav': nav, 'username':request.user.username, 'general_form':general_form, 'meeting_form':meeting_form, 'workout_form':workout_form, 'points':points, 'point_history': point_hist})
    return redirect_if_not_logged_in(request, callback)

def add_on_by_id(request, game_id):
    def callback(request):
        game = AddOnGame.objects.get(pk=game_id)
        entries = []
        for entry in AddOnEntry.objects.all().iterator():
            if entry.add_on_game == game_id:
                entries.append(entry)
        entries = sorted(entries, key=(lambda entry: entry.climb_in_game))
        nav = b_log_out + b_logged_in_as(request) + b_add_climb + ba_view_climbs + b_view_leaderboard
        form = CommentForm()
        entry_form = AddOnEntryForm()
        if request.method == 'POST':
            if 'comment_submission' in request.POST:
                form = CommentForm(request.POST)
                if form.is_valid():
                    obj = Comment.objects.create(\
                    comment = form.cleaned_data.get("comment"),\
                    climb_id = game_id,\
                    is_climb_comment = False)
                    obj.user = str(request.user)
                    obj.save()
                    return HttpResponseRedirect('/addson/' + str(game_id))
            elif 'entry_submission' in request.POST:
                entry_form = AddOnEntryForm(request.POST, request.FILES)
                if entry_form.is_valid():
                    obj = AddOnEntry.objects.create(\
                    picture = entry_form.cleaned_data.get("picture"),\
                    add_on_game = game_id,\
                    climb_in_game = len(entries) + 1)
                    obj.creator = str(request.user)
                    obj.save()
                    return HttpResponseRedirect('/addson/' + str(game_id))
            elif 'reset_report' in request.POST:
                obj = ResetReport.objects.create(climb_id=game_id,is_climb_complaint=False)
                obj.user = str(request.user)
                obj.save()
                return HttpResponseRedirect('/addson/' + str(game_id))
        comments = []
        for comment in Comment.objects.all().iterator():
            if comment.climb_id == game_id and not comment.is_climb_comment:
                comments.append(comment)
        if complained_add_on(game_id, request.user):
            reset = "<h2>This game's reset status is under review</h2>"
        else:
            reset = '<input type="submit", name="reset_report", value="I think this game has been reset.">'
        return render(request, 'add_on_details.html', {'game':game, 'account_nav':nav, 'comments':comments, 'comment_form':form, 'reset':reset, 'entries':entries, 'are_entries':len(entries) != 0, 'entry_form':entry_form})
    return redirect_if_not_logged_in(request, callback)

def climb_by_id(request, climb_id):
    def callback(request):
        climb = Climb.objects.get(pk=climb_id)
        annotate_completion(climb, request.user)
        nav = b_log_out + b_logged_in_as(request) + b_add_climb + ba_view_climbs + b_view_leaderboard
        form = CommentForm()
        if request.method == 'POST':
            if 'comment_submission' in request.POST:
                form = CommentForm(request.POST)
                if form.is_valid():
                    obj = Comment.objects.create(\
                    comment = form.cleaned_data.get("comment"),\
                    climb_id = climb_id)
                    obj.user = str(request.user)
                    obj.save()
                    return HttpResponseRedirect('/climbs/' + str(climb_id))
            elif 'completion' in request.POST:
                obj = ClimbComplete.objects.create(climb_id=climb_id)
                obj.user = str(request.user)
                obj.save()
                return HttpResponseRedirect('/climbs/' + str(climb_id))
            elif 'reset_report' in request.POST:
                obj = ResetReport.objects.create(climb_id=climb_id)
                obj.user = str(request.user)
                obj.save()
                return HttpResponseRedirect('/climbs/' + str(climb_id))
        if completed_climb(climb_id, request.user):
            submit = '<h2>You have completed this climb</h2>'
        else:
            submit = '<input type="submit", name="completion", value="I did this climb">'
        if complained_climb(climb_id, request.user):
            reset = "<h2>This climb's reset status is under review</h2>"
        else:
            reset = '<input type="submit", name="reset_report", value="I think this climb has been reset.">'
        comments = []
        for comment in Comment.objects.all().iterator():
            if comment.climb_id == climb_id and comment.is_climb_comment:
                comments.append(comment)
        return render(request, 'climb_details.html', {'climb':climb, 'account_nav':nav, 'comments':comments, 'submit':submit, 'comment_form':form, 'reset':reset})
    return redirect_if_not_logged_in(request, callback)

################
# TRIVIA PAGES #
################
def trivia_home(request):
    return render(request, 'trivia.html')


##############
# TEST PAGES #
##############

def loggedincheck(request):
    if request.user.is_authenticated:
        return render(request, 'loggedincheck.html', {'username':request.user.username, 'email':request.user.email})
    else:
        return render(request, 'loggedincheck.html', {'username':"NOT LOGGED IN", 'email':''})
