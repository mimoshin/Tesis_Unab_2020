from django.urls import path
from . import views

urlpatterns =[
    path('logistica',views.logistic_view,name='logistic_view'),
    path('logistica/calendarizar',views.request_day,name='request_day'),
    path('logistica/proyectos',views.projects_view,name='projects_view'),
    path('logistica/proyectos/nuevo',views.create_project,name='create_project'),
    #path('logistica/proyectos/ver/<int:p_pk>',views.review_project,name='review_project'),
    path('day',views.entry_event,name='entry_event'),
    
]