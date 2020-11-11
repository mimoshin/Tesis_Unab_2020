from django.contrib import admin
from .models import event_calendar,other_event
# Register your models here.
admin.site.register(event_calendar)
admin.site.register(other_event)