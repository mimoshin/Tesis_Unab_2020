from django.urls import path
from . import views

urlpatterns =[
    path('logistica',views.logistic_view,name='logistic_view'),
    path('day',views.request_day,name='day_request'),
]