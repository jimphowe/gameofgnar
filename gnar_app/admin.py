from django.contrib import admin

from .models import Climb, GeneralPoints, MeetingAttended, WorkoutAttended, ClimbComplete
admin.site.register(Climb)
admin.site.register(GeneralPoints)
admin.site.register(MeetingAttended)
admin.site.register(WorkoutAttended)
admin.site.register(ClimbComplete)
