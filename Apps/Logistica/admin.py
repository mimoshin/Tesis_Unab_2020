from django.contrib import admin
from .models import*
# Register your models here.
admin.site.register(event_calendar)
admin.site.register(other_event)
admin.site.register(Dep_event)
admin.site.register(Ind_event)