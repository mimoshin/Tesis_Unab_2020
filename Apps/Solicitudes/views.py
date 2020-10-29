from django.shortcuts import render, redirect, HttpResponse
from .models import Event_Request
from Login.models import Admin,Client


#:::::::::::::::::::Functions:::::::::::::::::::::
def load_notify():
    notify_list = ["notificacion 1","notificacion 2","notificacion 3","notificacion 4","notificacion 5"]
    return notify_list

def load_message():
    messages_list = {"mensaje 1","mensaje 2","mensaje 3","mensaje 4","mensaje 5"}
    return messages_list

def load_data(user,kwargs = None):
    u_messages = load_message()
    u_notify = load_notify()
    data = {'profile':user,'u_notify':u_notify,'u_messages':u_messages,'kwargs':kwargs}
    return data

def load_data_2(kwargs = None):
    u_messages = load_message()
    u_notify = load_notify()
    data = {'u_notify':u_notify,'u_messages':u_messages,'kwargs':kwargs}
    return data

def load_client(user):
    client = Client.objects.get(client_person=user)
    return client
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::General_Views:::::::::::::::::
#Requests_view
def requests_view(request):
    user_log = request.user
    admin = Admin.objects.filter(admin_person__username = user_log ).exists()
    client = Client.objects.filter( client_person__username = user_log ).exists()
    if request.method == 'POST':
        if admin:
            return admin_requests(request)
        if client:
            return client_requests(request)
    if request.method == 'GET':
        if admin:
            return admin_requests(request)
        if client:
            return client_requests(request)
    return redirect('/')

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Admin_Views:::::::::::::::::::
#Admin_requests_view
def admin_requests(request):
    requests_list = Event_Request.objects.all()
    data = load_data_2(requests_list)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/admin_requests.html',data)

#Admin_review_request
def review_request(request,pk_id):
    object_request = Event_Request.objects.get(pk=pk_id)
    data = load_data_2(object_request)
    if request.method == 'POST':
        d_rcvd = request.POST
        if d_rcvd['estado']:
            object_request.status = d_rcvd['estado']
            object_request.save()
        else:
            pass
        return HttpResponse('hola')
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/review_request.html',data)

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::

#Client_request_view
def client_requests(request):
    pk = request.user.pk
    requests_list = Event_Request.objects.filter(petitioner__client_person__pk=pk)
    data = load_data_2(requests_list)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/client_requests.html',data)

#New_event_request
def new_event_request(request):
    data = load_data_2()
    if request.method == 'POST':
        r_form = request.POST
        client = load_client(request.user)
        n_request = Event_Request(petitioner=client,event_title=r_form['event_title'],event_type=r_form['event_type'],event_place=r_form['event_place'],event_date=r_form['event_date'],
                    init_hour=r_form['init_hour'],finish_hour=r_form['finish_hour'], text=r_form['spe_ev'],status="Necesita revision")  
        n_request.save()
        print(r_form)
        print(r_form['event_date'],r_form['init_hour'],r_form['finish_hour'])
        return redirect('requests_views')
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/new_client_e_request.html',data)

#New_info_request
def New_info_request(request):
    data = load_data_2()
    if request.method == 'POST':
        r_form = request.POST
        return redirect('requests_views')
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/new_client_i_request.html',data)

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::