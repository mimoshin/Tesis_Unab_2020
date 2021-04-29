from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from datetime import date
from Login.models import User_Factory
from Solicitudes.models import Request_Factory
from Eventos.models import Event_factory
from .models import Calendar_Factory,project
from .utilities import calendar_month, load_day, load_events_day,get_data_time




#:::::::::::::::::::Functions:::::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::General_Views:::::::::::::::::
def logistic_view(request):
    user_log = User_Factory.get_type_user(request.user)
    if user_log == 'admin':
        return admin_logistic(request)
    elif user_log == 'client':
        return client_logistic(request)
    return render(request,'/')

def projects_view(request):
    user_log = User_Factory.get_type_user(request.user)
    if user_log == 'admin':
        return admin_projects(request)
    elif user_log == 'client':
        return client_projects(request)
    return render(request,'/')
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Admin_Views:::::::::::::::::::
def admin_logistic(request):
    if request.method == 'POST':
        dates = get_data_time()
        if request.POST.get('consulta'):
            data = Calendar_Factory.get_events(dates['month'],dates['year'])
            return HttpResponse(data)

    elif request.method == 'GET':
        d_recvd = request.GET
        month,year = d_recvd.get('month'), d_recvd.get('year')
        if month and year:
            print("Cargando: data_time", month,year)
            dates = get_data_time(Month=month,Year=year)
        else:
            print("Cargando: data_time")
            dates = get_data_time()

    print("Data_time: ",dates)
    events = Calendar_Factory.get_all(dates['month'],dates['year'])
    print("Eventos",events)
    aux = calendar_month(dates['year'],dates['month'],events,dates)
    return render(request,'Logistica/admin_calendar.html',{'calendar':aux['calendar'],'disponibility':aux['disp_days']})

def admin_projects(request):
    projects = project.objects.all()
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Logistica/proyectos/admin_projects.html',{'kwargs':projects})

def create_project(request):
    data = 'data'
    if request.method == 'POST':
        data_form = request.POST
        print(data_form)
        new_project = project(project_title=data_form['title'],date_init=data_form['init'],date_finish=data_form['finish'],details=data_form['details'])
        new_project.save()
        return redirect('projects_view')
    if request.method == 'GET':
        pass
    return render(request,'Logistica/proyectos/new_project.html',{'kwargs':data})

def request_day(request):
    """
    Consulta los eventos del dia indicado mediante una peticion POST
    Retorna una lista que contiene la disponibilidad horaria del dia
    """
    if request.method == 'POST':
        date= request.POST.get('date')
        events_list = Calendar_Factory.get_all_day(date)
        total = len(events_list)
        if total == 0:
            day_hours = load_day()
            return HttpResponse(day_hours)
            #return JsonResponse(data_day,safe=False)
        elif total > 0:
            day_hours = load_events_day(events_list)
            return HttpResponse(day_hours)
            #return JsonResponse(day_hours,safe=False)
        else:
            print("Hay eventos: ",len(events_list))
        
    if request.method == 'GET':
        pass
    return redirect('/solicitudes')

#entry_event_view
def entry_event(request):
    """
    Crea el evento en el calendario de logistica relacionando el evento y la solicitud
    """
    if request.method == 'POST':
        form_data = request.POST
        validation = form_data.get('request')
        if validation:
            """
            1° Obtener los datos de la solicitud | Solicitudes - Request_Factory | Object: Event_request
            2° Crear evento con los datos de la solicitud | Eventos - Event_Factory | Object: Event_[TYPE_EVENT]
            3° Calendariza el evento | Logistica - Calendar_Factory | Void
            """
            _id_ = form_data.get('id_request')
            request_data = Request_Factory.get_request('event',_id_)
            new_event = Event_factory.create_event(organizer='client',request=request_data)
            Calendar_Factory.create_event('Dep',request_data,request.user,new_event)
            request_data.set_status('0')
            #Request_Factory.set_estatus(request_data,'0',request.user)
            return HttpResponse('Creacion Correcto')    
                
        else:
            """
            1° Crear evento cargando los datos del formulario | organizer = admin
            3° Calendariza el evento | Logistica - Calendar_Factory | Void
            """
            #organizer = User_Factory.get_client(form_data['client_pk'])
            #new_event = Event_factory.create_event(organizer='admin',form=form_data,user=request.user.pk)
            new_event = Event_factory.create_event(organizer='admin',form=form_data,user=request.user.pk)
            Calendar_Factory.create_event('Ind','NoRequest',request.user,new_event)
        
    if request.method == 'GET':
        pass
    return redirect('/Logistica')
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::
def client_logistic(request):
    pk = request.user.pk
    if request.method == 'POST':
        dates = get_data_time()
        if request.POST.get('consulta'):
            data = Calendar_Factory.get_events(dates['month'],dates['year'])
            return HttpResponse(data)
            
    elif request.method == 'GET':
        d_recvd = request.GET
        month,year = d_recvd.get('month'), d_recvd.get('year')
        if month and year:
            dates = get_data_time(Month=month,Year=year)
        else:
            dates = get_data_time()
        
    #events = Calendar_Factory.get_all(dates['month'],dates['year'])
    events = Calendar_Factory.get_client_events(pk,dates['month'],dates['year'])
    aux = calendar_month(dates['year'],dates['month'],events,dates)
    return render(request,'Logistica/client_calendar.html',{'calendar':aux['calendar'],'disponibility':aux['disp_days']})

def client_projects(request):
    projects = project.objects.all()
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Logistica/proyectos/client_projects.html',{'kwargs':projects})
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::
