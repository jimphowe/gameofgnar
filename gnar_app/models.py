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

class Climb(models.Model):
    grade = models.PositiveIntegerField()
    location = models.CharField(max_length=15,choices=GYMS)
    time_added = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to = "media")
    creator = models.CharField(max_length=30)
