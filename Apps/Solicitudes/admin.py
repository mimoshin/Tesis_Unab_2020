from django.contrib import admin
from .models import Info_request,Event_request
# Register your models here.

admin.site.register(Event_request)
admin.site.register(Info_request)

