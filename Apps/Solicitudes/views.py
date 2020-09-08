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

def load_data(usuario,kwargs = None):
    u_messages = load_message()
    u_notify = load_notify()
    data = {'profile':usuario,'u_notify':u_notify,'u_messages':u_messages,'kwargs':kwargs}
    return data

def load_data_2(kwargs = None):
    u_messages = load_message()
    u_notify = load_notify()
    data = {'u_notify':u_notify,'u_messages':u_messages,'kwargs':kwargs}
    return data
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
    requests_list = Event_Request.objects.filter(petitioner__pk=pk)
    data = load_data_2(requests_list)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/client_requests.html',data)

#New_request
def new_request(request):
    data = load_data_2()
    if request.method == 'POST':
        n_request = Event_Request(petitioner= request.user,text=request.POST['readya_text'],status="Necesita revision")
        n_request.save()
        return redirect('requests_views')
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/new_client_request.html',data)

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::