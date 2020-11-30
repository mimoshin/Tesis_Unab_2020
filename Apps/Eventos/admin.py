from django.contrib import admin
from .models import Team_championship, Single_championship, Other_event, Athlete, Athlete_team, Other_person, Team
# Register your models here.
admin.site.register(Team_championship)
admin.site.register(Single_championship)
admin.site.register(Other_event)
admin.site.register(Athlete)
admin.site.register(Athlete_team)
admin.site.register(Other_person)
admin.site.register(Team)
