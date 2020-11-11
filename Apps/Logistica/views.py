from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from Login.models import Client,Admin
from Solicitudes.models import Event_Request
from .models import event_calendar,other_event
from .utilities import calendar_month,load_day,load_events_day
from datetime import date



#:::::::::::::::::::Functions:::::::::::::::::::::
def load_events(month,year):
    month_filter = r'{0}-{1}-.*'.format(str(year),str(month))
    event_list = list(other_event.objects.filter(e_request__event_date__regex = month_filter))
    return event_list

def load_client_event(client_pk):
    event_list = list(other_event.objects.filter(e_request__petitioner__client_person__pk=client_pk))
    print('holi')
    for x in event_list:
        print('holi',x)
    return event_list

def events_day(filter_day):
    month_filter = r'{0}'.format(filter_day)
    event_list = list(other_event.objects.filter(e_request__event_date__regex = month_filter))
    return event_list

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::General_Views:::::::::::::::::
def logistic_view(request):
    user_log = request.user
    admin = Admin.objects.filter(admin_person__username = user_log ).exists()
    client = Client.objects.filter( client_person__username = user_log ).exists()
    if request.method == 'POST':
        if admin:
            return admin_logistic(request)
        if client:
            return client_logistic(request)
    if request.method == 'GET':
        if admin:
            return admin_logistic(request)
        if client:
            return client_logistic(request)
        return redirect('/')
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Admin_Views:::::::::::::::::::
def admin_logistic(request):
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
        
        events = load_events(month,year)
        aux = calendar_month(year,month,events)
            
    return render(request,'Logistica/admin_calendar.html',{'calendar':aux['calendar'],'next':next_month,'prev':prev_month,'year':year,
                          'prev_year':prev_year,'next_year':next_year,'events':events,'disponibility':aux['disp_days']})

def request_day(request):
    if request.method == 'POST':
        d_recvd = request.POST
        pk_request = d_recvd.get('pk_request')
        event_data = Event_Request.objects.get(pk=pk_request)
        events_list = events_day(event_data.event_date)
        total = len(events_list)
        if total == 0:
            day_hours = load_day()
            return HttpResponse(day_hours)
        elif total > 0:
            print()
            day_hours = load_events_day(events_list)
            return HttpResponse(day_hours)
        
        else:
            print("Hay eventos: ",len(events_list))
        
        #aux = calendar_month(year,month,events)
        
    if request.method == 'GET':
        pass
    return redirect('/solicitudes')

def entry_event(request):
    if request.method == 'POST':
        d_recvd = request.POST
        pk_request = d_recvd.get('e_request')
        request_data = Event_Request.objects.get(pk=pk_request)
        request_data.set_status('0')
        new_event = other_event(e_request=request_data)
        new_event.save()
        return HttpResponse('holi')    
        
    if request.method == 'GET':
        pass
    return redirect('/solicitudes')

    

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
        
        events = load_client_event(pk)
        aux = calendar_month(year,month,events)
            
    return render(request,'Logistica/client_calendar.html',{'calendar':aux['calendar'],'next':next_month,'prev':prev_month,'year':year,
                          'prev_year':prev_year,'next_year':next_year,'events':events,'disponibility':aux['disp_days']})


#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::
