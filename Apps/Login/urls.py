from django.urls import path
from . import views

urlpatterns =[
    path('',views.start,name='inicio'),
    path('ingreso',views.entry,name='ingreso'),
    path('index',views.index,name='index'),
]   