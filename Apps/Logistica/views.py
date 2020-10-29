from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from Login.models import Client,Admin
from .models import event_calendar
from .utilities import calendar_month
from datetime import date

#:::::::::::::::::::Variables:::::::::::::::::::::
hours = ['8:00 - 9:00 hrs','9:00 - 10:00 hrs','10:00 - 11:00 hrs','11:00 - 12:00 hrs','13:00 - 14:00 hrs',
             '15:00 - 16:00 hrs','16:00 - 17:00 hrs','17:00 - 18:00 hrs','18:00 - 19:00 hrs','20:00 - 21:00 hrs',
             '21:00 - 22:00 hrs','22:00 - 23:00 hrs','23:00 - 24:00 hrs']
class evento():
    def __init__(self,titulo,inicio,fin,zona,dia):
        self.mes = 10
        self.titulo = titulo
        self.inicio =  inicio
        self.fin = fin
        self.zona = zona
        self.dia = dia

eventos_custom = [evento('torneo cs',8,20,'multicancha',10),
                  evento('torneo don miguel',10,23,'pista',11),
                  evento('torneo futball',16,20,'sintetica',10),
                  evento('torneo nado',15,20,'piscina',10),
                 ]
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Functions:::::::::::::::::::::
def load_calendar(month):
    months=['Enero','Febrero','Marzo','Abril','Mayo','Junio',
            'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    list_event = list(event_calendar.objects.all())
    eventos = []
    for x in list_event:
        date = x.date.split(' ')
        if date[1] in months[month-1]:
            eventos.append(x)
    return eventos
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
        res = request.POST

    if request.method == 'GET':
        if request.GET:
            res = request.GET
            if res['month']:
                month = int(res['month'])
                prev_month = int(month)-1
                next_month = int(month)+1
            else:
                month = int(today.month)
                prev_month = int(today.month)-1
                next_month = int(today.month)+1

        else: 
            month = int(today.month)
            prev_month = int(today.month)-1
            next_month = int(today.month)+1
        
        events = load_calendar(month)
        calendar = calendar_month(2020,month,events)
        for x in events:
            print(x.event)
            
    return render(request,'Logistica/admin_calendar.html',{'calendar':calendar,'next':next_month,'prev':prev_month,'hours':hours,
                                                           'events':events,'customs':eventos_custom})

def request_day(request):
    if request.method == 'POST':
        return HttpResponse("hola")

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::
def client_logistic(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Logistica/client_calendar.html')
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::
