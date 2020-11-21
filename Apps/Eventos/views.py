from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from Login.utilities import type_user,load_data
from .models import Event_factory,Athlete_factory,team

#:::::::::::::::::::Functions:::::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::General_Views:::::::::::::::::
def events_view(request):
    user_log = type_user(request.user)

    if user_log == 'admin':
        return admin_events(request)

    elif user_log == 'client':
        return client_events(request)
    else:
        return redirect('/')

def question_teams(request):
    if request.method == 'POST':
        id_event = request.POST.get('event')
        teams = list(team.objects.filter(event=id_event).values())
        if id_event:
            return JsonResponse(teams, safe=False)
    elif request.method == 'GET':
        pass

def question_athlete(request):
    if request.method == 'POST':
        id_event = request.POST.get('event')
        athletes = Athlete_factory.get_athlete_event('single',id_event)
        if id_event:
            return JsonResponse(athletes, safe=False)
    elif request.method == 'GET':
        pass

def question_person(request):
    if request.method == 'POST':
        id_event = request.POST.get('event')
        persons = Athlete_factory.get_athlete_event('other',id_event)
        if id_event:
            return JsonResponse(persons, safe=False)
    elif request.method == 'GET':
        pass
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Admin_Views:::::::::::::::::::
#Admin_events--view
def admin_events(request):
    events = Event_factory.get_all()
    data = load_data(events)
    if request.method == 'POST':
        if request.POST.get('single'):
            event = Event_factory.create_event('single_championship')
            event.save()

        elif request.POST.get('other'):
            event = Event_factory.create_event('other_event')
            event.save()

        elif request.POST.get('team'):
            event = Event_factory.create_event('team_championship')
            event.save()
        return HttpResponse('hola si funciona')

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
    events = Event_factory.get_all()
    data = load_data(events)
    if request.method == 'POST':
        if request.POST.get('single'):
            event = Event_factory.create_event('single_championship')
            event.save()

        elif request.POST.get('other'):
            event = Event_factory.create_event('other_event')
            event.save()

        elif request.POST.get('team'):
            event = Event_factory.create_event('team_championship')
            event.save()
        return HttpResponse('hola si funciona')

    elif request.method == 'GET':
        pass
    
    return render(request,'Eventos/client_events.html',data)

#Client_review_event--view
def review_event(request,e_type,e_id):
    templates = {'team':'Eventos/client_view_team_event.html','single':'Eventos/client_view_single_event.html',
                 'other':'Eventos/client_view_other_event.html'}
    event = Event_factory.get_event(e_type,e_id)
    data = load_data(event)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    return render(request,templates[e_type],data)
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::
