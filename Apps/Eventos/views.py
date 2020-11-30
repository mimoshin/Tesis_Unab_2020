from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from Login.models import User_Factory
from Login.utilities import load_data
from .models import Event_factory,Athlete_factory,Team_Factory

#:::::::::::::::::::Functions:::::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::General_Views:::::::::::::::::
def events_view(request):
    user_log = User_Factory.get_type_user(request.user)
    if user_log == 'admin':
        return admin_events(request)

    elif user_log == 'client':
        return client_events(request)
    else:
        return redirect('/')

def question_teams(request):
    if request.method == 'POST':
        id_event = request.POST.get('event')
        teams = Team_Factory.get_event_teams(id_event)
        if id_event:
            return JsonResponse(teams, safe=False)
    elif request.method == 'GET':
        pass

def question_athlete(request):
    if request.method == 'POST':
        id_event = request.POST.get('event')
        athletes = Athlete_factory.get_athletes(type='single',id_event=id_event)
        print(athletes)
        if id_event:
            return JsonResponse(athletes, safe=False)
    elif request.method == 'GET':
        pass

#Question_person--NotView
def question_person(request):
    if request.method == 'POST':
        id_event = request.POST.get('event')
        persons = Athlete_factory.get_athletes(type='other',event=id_event)
        return JsonResponse(persons, safe=False)
    elif request.method == 'GET':
        pass
#View_inscriptions_team--View
def view_team(request,id_team):
    """Vista para ver un equipo"""
    team = Team_Factory.get_team(id_team)
    athletes = Athlete_factory.get_athletes(type='team',team=id_team)
    data = load_data(team,athletes=athletes)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    return render(request,'Eventos/inscriptions/client_view_team.html',data)
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Admin_Views:::::::::::::::::::
#Admin_events--view
def admin_events(request):
    events = Event_factory.get_all()
    data = load_data(events)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    return render(request,'Eventos/admin_events.html',data)

#Admin_view_event--view
def view_event(request,e_type,e_id):
    templates = {'team':'Eventos/admin_view_team_event.html','single':'Eventos/admin_view_single_event.html',
                 'other':'Eventos/admin_view_other_event.html'}
    event = Event_factory.get_event(e_type,e_id)
    data = load_data(event)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    return render(request,templates[e_type],data)

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::
#Client_events--view
def client_events(request):
    pk = request.user.pk
    events = Event_factory.get_my_events(pk)
    data = load_data(events)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    return render(request,'Eventos/client_events.html',data)

#Client_review_event--view
def review_event(request,e_type,e_id):
    """Vista para revisar un evento"""
    templates = {'team':'Eventos/client_view_team_event.html','single':'Eventos/client_view_single_event.html',
                 'other':'Eventos/client_view_other_event.html'}               
    event = Event_factory.get_event(e_type,e_id)
    data = load_data(event)
    if request.method == 'POST':
        form_data = request.POST
        if form_data.get('observation'):
            Event_factory.set_observation(form_data['observation'],event=event)
        elif form_data.get('team_name'):
            Team_Factory.create_team(data=form_data,event=event)
    elif request.method == 'GET':
        pass
    return render(request,templates[e_type],data)

#Client_team_inscription--view
def team_inscription(request,id_team):
    """Viesta completa para la inscripcion de un equipo"""
    team = Team_Factory.get_team(id_team)
    athlete_list = Athlete_factory.get_athletes(type='team',team=id_team)
    data = load_data(team,athletes=athlete_list)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    return render(request,'Eventos/Inscriptions/team_inscription.html',data)
    
#Client_athlete_team_inscription--Noview
def team_athlete(request):
    """Vista para la inscripcion de un deportista equipo"""
    if request.method == 'POST':
        form_data = request.POST
        team = Team_Factory.get_team(form_data['id_team'])
        Athlete_factory.create_athlete(type='team',form=form_data,team=team)
        Team_Factory.set_max(team.pk,form_data['position'])
        return redirect('/eventos/inscribir/equipo/%s' % (form_data['id_team']))
    elif request.method == 'GET':
        return redirect('/eventos')

#Client_athlete_inscription--Noview
def athlete_inscription(request):
    """Vista para la inscripcion de un deportista a un torneo"""
    if request.method == 'POST':
        form_data = request.POST
        print(form_data)
        event = Event_factory.get_event('single',form_data['id_event'])
        Athlete_factory.create_athlete(type='single',form=form_data,event=event)
        return redirect('/eventos/revisar/single/%s' % (form_data['id_event']))
    elif request.method == 'GET':
        return redirect('/eventos')

#Client_person_inscription--Noview
def person_inscription(request):
    """Vista para la inscripcion de una persona a un evento"""
    if request.method == 'POST':
        form_data = request.POST
        event = Event_factory.get_event('other',form_data['id_event'])
        Athlete_factory.create_athlete(type='other',form=form_data,event=event)
        return redirect('/eventos/revisar/other/%s' % (form_data['id_event']))
    elif request.method == 'GET':
        return redirect('/eventos')
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::
