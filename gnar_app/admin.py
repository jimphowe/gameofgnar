from django.contrib import admin

from .models import Climb, GeneralPoints, MeetingAttended, WorkoutAttended, ClimbComplete, MiscellaneousPoints, Comment, ResetReport, AddOnGame, AddOnEntry
admin.site.register(Climb)
admin.site.register(GeneralPoints)
admin.site.register(MeetingAttended)
admin.site.register(WorkoutAttended)
admin.site.register(ClimbComplete)
admin.site.register(MiscellaneousPoints)
admin.site.register(Comment)
admin.site.register(ResetReport)
admin.site.register(AddOnGame)
admin.site.register(AddOnEntry)
