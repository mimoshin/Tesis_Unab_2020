from django.urls import path
from . import views

urlpatterns =[
    path('',views.logistic_view,name='logistic_view'),
    path('calendarizar',views.request_day,name='request_day'),
    path('proyectos',views.projects_view,name='projects_view'),
    path('proyectos/nuevo',views.create_project,name='create_project'),
    #path('logistica/proyectos/ver/<int:p_pk>',views.review_project,name='review_project'),
    path('day',views.entry_event,name='entry_event'), # AQUI
]