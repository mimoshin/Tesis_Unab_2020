from django.urls import path
from . import views

urlpatterns =[
    path('logistica',views.logistic_view,name='logistic_view'),
    path('logistica/calendarizar',views.request_day,name='request_day'),
    path('day',views.entry_event,name='entry_event'),
]