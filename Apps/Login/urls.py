from django.urls import path
from . import views

urlpatterns =[
    path('',views.start,name='inicio'),
    path('ingreso',views.entry,name='ingreso'),
    path('index',views.index,name='index'),
    path('registrar',views.register,name='registro'),
    path('modificar/<int:pkid>',views.modify,name='modificar'),
    path('eliminar/<int:pkid>',views.delete,name='eliminar'),
    path('logout',views.user_logout,name='salir'),
]   