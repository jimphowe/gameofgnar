from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

GYMS = [
    #first tuple val goes in db, second is display
    ('Boston','Boston'),
    ('Cambridge','Cambridge'),
    ('Watertown','Watertown'),
    ('Stoneham','Stoneham'),
    ('Randolph','Randolph')
]

WORKOUTS = [
        (1,'January 28th'),
        (2,'February 4th'),
        (3,'February 11th'),
        (4,'February 18th'),
        (5,'February 25th'),
]

MEETINGS = [
        (1, 'February 2nd'),
        (2, 'February 16th'),
        (3, 'March 2nd'),
]

GENERAL_POINTS = [
        (1, 'Strange beta'),
        (2, 'Breakfast at open'),
        (3, 'Snack given to teammate'),
]

class WorkoutAttended(models.Model):
    user = models.CharField(max_length=30)
    date = models.PositiveIntegerField(choices=WORKOUTS)

class MeetingAttended(models.Model):
    user = models.CharField(max_length=30)
    date = models.PositiveIntegerField(choices=MEETINGS)

class MeetingGameWon(models.Model):
    user = models.CharField(max_length=30)
    date = models.PositiveIntegerField(choices=MEETINGS)

class GeneralPoints(models.Model):
    user = models.CharField(max_length=30)
    location = models.CharField(max_length=15,choices=GYMS)
    time_added = models.DateTimeField(auto_now_add=True)
    kind = models.PositiveIntegerField(choices=GENERAL_POINTS)

class MiscellaneousPoints(models.Model):
    user = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    time_added = models.DateTimeField(auto_now_add=True)
    points = models.PositiveIntegerField()

class Climb(models.Model):
    grade = models.PositiveIntegerField()
    location = models.CharField(max_length=15,choices=GYMS)
    time_added = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(default='image.jpg',upload_to = "media")
    creator = models.CharField(max_length=30)
    reset = models.BooleanField(default=False)

class ClimbComplete(models.Model):
    user = models.CharField(max_length=30)
    climb_id = models.PositiveIntegerField()
    time_added = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.CharField(max_length=30)
    comment = models.CharField(max_length=300)
    climb_id = models.PositiveIntegerField()
    time_added = models.DateTimeField(auto_now_add=True)
    is_climb_comment = models.BooleanField(default=True)

class ResetReport(models.Model):
    user = models.CharField(max_length=30)
    climb_id = models.PositiveIntegerField()
    time_added = models.DateTimeField(auto_now_add=True)
    is_climb_complaint = models.BooleanField(default=True)

class AddOnGame(models.Model):
    creator = models.CharField(max_length=30)
    time_added = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveIntegerField()
    location = models.CharField(max_length=15,choices=GYMS)
    reset = models.BooleanField(default=False)

class AddOnEntry(models.Model):
    time_added = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(default='image.jpg',upload_to = "media")
    creator = models.CharField(max_length=30)
    add_on_game = models.PositiveIntegerField()
    climb_in_game = models.PositiveIntegerField()



"""
class AddOn(models.Model):
    grade = models.PositiveIntegerField()
    location = models.Charfield(max_length=15,choices=GYMS)
    time_added = models.DateTimeField(auto_now_add=True)

class AddOnEntry(models.Model):
    add_on = models.ForeignKey(AddOn, null=True, default=None)
    order = models.IntegerField()
    time_added = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(default='image.jpg',upload_to = "media")
    creator = models.CharField(max_length=30)

    class Meta:
        unique_together=('add_on', 'order')
        """
