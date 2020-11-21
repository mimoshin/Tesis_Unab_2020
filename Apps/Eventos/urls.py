from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('eventos',views.events_view,name='events_view'),#index de eventos
   path('eventos/ver/<str:e_type>/<int:e_id>',views.view_event,name='view_event'),#ver evento Admin
   path('eventos/revisar/<str:e_type>/<int:e_id>',views.review_event,name='review_event'),#revisar evento Client
   path('eventos/question_teams',views.question_teams,name='question_teams'),#consultar equipos asociados a un torneo por equipos
   path('eventos/question_athlete',views.question_athlete,name='question_athlete'),#consultar atletas inscritos a un torneo individual
   path('eventos/question_aperson',views.question_person,name='question_person')#consultar participantes inscritos a un evento
]