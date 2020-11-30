from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from datetime import date
from Login.models import User_Factory
from Solicitudes.models import Request_Factory
from Eventos.models import Event_factory
from .models import Calendar_Factory,project
from .utilities import calendar_month, load_day, load_events_day




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
    today = date.today()
    if request.method == 'POST':
        year = int(today.year)
        month = int(today.month)
        if request.POST.get('consulta'):
            data = Calendar_Factory.get_events(month,year)
            return HttpResponse(data)
    if request.method == 'GET':
        d_recvd = request.GET
        if d_recvd.get('month') and d_recvd.get('year'):
            Month,Year = d_recvd['month'],d_recvd['year']
            if Month:
                month = int(Month)
                if month == 12:
                    prev_month = month-1
                    next_month = 1
                    year = int(Year)
                    next_year = year+1
                    prev_year = int(year)-1
                    
                elif month == 1:
                    prev_month = 12
                    next_month = month+1
                    year = int(Year)
                    next_year = int(year)+1
                    prev_year = int(year)-1
                    
                else:
                    prev_month = month-1
                    next_month = month+1
                    year = int(Year)
                    next_year = year+1
                    prev_year = int(year)-1
                
            else:
                year = int(today.year)
                next_year = year+1
                prev_year = int(year)-1
                month = int(today.month)
                prev_month = int(today.month)-1
                next_month = int(today.month)+1
                
        else: 
            year = int(today.year)
            next_year = year+1
            prev_year = int(year)-1
            month = int(today.month)
            prev_month = int(today.month)-1
            next_month = int(today.month)+1
            #print("año: {0}  proximo año {1} mes: {2} proximo mes: {3} mes anterior: {4}".format(year,next_year,month,next_month,prev_month))

        data = {'year':year,'next_year':next_year,'prev_year':prev_year,
                'month':month,'prev_month':prev_month,'next_month':next_month}

        events = Calendar_Factory.get_all(month,year)
        aux = calendar_month(year,month,events,data)
            
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

def entry_event(request):
    if request.method == 'POST':
        form_data = request.POST
        pk_request = form_data.get('e_request')
        if pk_request == 'NoRequest':
            #organizer = User_Factory.get_client(form_data['client_pk'])
            new_event = Event_factory.create_event(request='NoRequest',form=form_data)
            print('creando evento')
            Calendar_Factory.create_event('Ind','NoRequest',request.user,new_event)
        else:
            request_data = Request_Factory.get_request('event',pk_request)
            new_event = Event_factory.create_event(request=request_data)
            Calendar_Factory.create_event('Dep',request_data,request.user,new_event)
            request_data.set_status('0')
            return HttpResponse('Creacion Correcto')    
        
    if request.method == 'GET':
        pass
    return redirect('/logistica')

    

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::
def client_logistic(request):
    pk = request.user.pk
    today = date.today()
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        d_recvd = request.GET
        if d_recvd.get('month') and d_recvd.get('year'):
            Month,Year = d_recvd['month'],d_recvd['year']
            if Month:
                month = int(Month)
                if month == 12:
                    prev_month = month-1
                    next_month = 1
                    year = int(Year)
                    next_year = year+1
                    prev_year = int(year)-1
                    
                elif month == 1:
                    prev_month = 12
                    next_month = month+1
                    year = int(Year)
                    next_year = int(year)+1
                    prev_year = int(year)-1
                    
                else:
                    prev_month = month-1
                    next_month = month+1
                    year = int(Year)
                    next_year = year+1
                    prev_year = int(year)-1
                
            else:
                year = int(today.year)
                next_year = year+1
                prev_year = int(year)-1
                month = int(today.month)
                prev_month = int(today.month)-1
                next_month = int(today.month)+1
                
        else: 
            year = int(today.year)
            next_year = year+1
            prev_year = int(year)-1
            month = int(today.month)
            prev_month = int(today.month)-1
            next_month = int(today.month)+1
            #print("año: {0}  proximo año {1} mes: {2} proximo mes: {3} mes anterior: {4}".format(year,next_year,month,next_month,prev_month))

        data = {'year':year,'next_year':next_year,'prev_year':prev_year,
                'month':month,'prev_month':prev_month,'next_month':next_month}                
        events = Calendar_Factory.get_client_events(pk,month,year)
        aux = calendar_month(year,month,events,data)
            
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
