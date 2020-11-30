from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   path('eventos',views.events_view,name='events_view'),#index de eventos
   path('eventos/ver/<str:e_type>/<int:e_id>',views.view_event,name='view_event'),#ver evento Admin
   path('eventos/revisar/<str:e_type>/<int:e_id>',views.review_event,name='review_event'),#revisar evento Client  
   path('eventos/question_teams',views.question_teams,name='question_teams'),#consultar equipos asociados a un torneo por equipos
   path('eventos/question_athlete',views.question_athlete,name='question_athlete'),#consultar atletas inscritos a un torneo individual
   path('eventos/question_aperson',views.question_person,name='question_person'),#consultar participantes inscritos a un evento
   path('eventos/inscribir/equipo/<int:id_team>',views.team_inscription,name='team_inscription'), #Inscribir equipo a evento
   path('eventos/inscribir/equipo/deportista',views.team_athlete,name='team_athlete'), #Inscribir deportista a equipo
   path('eventos/inscribir/deportista',views.athlete_inscription,name='athlete_inscription'), #Inscribir deportista a evento
   path('eventos/inscribir/participante',views.person_inscription,name='person_inscription'), #Inscribir persona a evento
   path('eventos/inscritos/equipo/<int:id_team>',views.view_team,name='view_team'),
]