from django.shortcuts import render, redirect, HttpResponse
from .models import Event_Request,Info_request
from .forms import pruebaForm, otroForm
from Login.models import Admin,Client


#:::::::::::::::::::Functions:::::::::::::::::::::
def load_client_requests(pk):
    r_list = []
    first = Event_Request.objects.filter(petitioner__client_person__pk=pk)
    second = Info_request.objects.filter(petitioner__client_person__pk=pk)
    for x in first:
        r_list.append(x)
    for y in second:
        r_list.append(y)
    return r_list

def total_requests():
    r_list = []
    first = Event_Request.objects.all()
    second = Info_request.objects.all()
    for x in first:
        r_list.append(x)
    for y in second:
        r_list.append(y)
    return r_list

def load_notify():
    notify_list = ["notificacion 1","notificacion 2","notificacion 3","notificacion 4","notificacion 5"]
    return notify_list

def load_data_2(kwargs = None):
    u_notify = load_notify()
    data = {'u_notify':u_notify,'kwargs':kwargs}
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
    requests_list = total_requests()
    data = load_data_2(requests_list)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/admin_requests.html',data)

#Admin_review_filter
def review_request(request,pk_id,r_type):
    if r_type == 0:
        return review_request_event(request,pk_id)
    elif r_type == 1:
        return review_request_info(request,pk_id)


#Admin_review_request_event
def review_request_event(request,pk_id):
    object_request = Event_Request.objects.get(pk=pk_id)
    data = load_data_2(object_request)
    if request.method == 'POST':
        d_rcvd = request.POST
        stat_obs = d_rcvd.get('estado'),d_rcvd.get('observation')
        if stat_obs[0]:
            object_request.set_status(stat_obs[0])
            return HttpResponse('hola')
        elif stat_obs[1]:
            object_request.create_obs(stat_obs[1])
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/admin_review_event.html',data)

#Admin_review_request_info
def review_request_info(request,pk_id):
    object_request = Info_request.objects.get(pk=pk_id)
    data = load_data_2(object_request)
    if request.method == 'POST':
        d_rcvd = request.POST
        response = d_rcvd.get('response')
        stat_obs = d_rcvd.get('estado'),d_rcvd.get('observation')
        if stat_obs[0]:
            object_request.set_status(stat_obs[0])
            return HttpResponse('hola')
        elif stat_obs[1]:
            object_request.create_obs(stat_obs[1])
        elif response:
            object_request.set_response(response)
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/admin_review_info.html',data)

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::

#Client_request_view
def client_requests(request):
    pk = request.user.pk
    requests_list = load_client_requests(pk)
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
        date_format = r_form['event_date']
        print(date_format)
        n_request = Event_Request(petitioner=client,event_title=r_form['event_title'],event_type=r_form['event_type'],event_place=r_form['event_place'],
                                  status="Necesita revision",specification=r_form['spe_ev'],event_date=r_form['event_date'],init_hour=r_form['init_hour'],finish_hour=r_form['finish_hour'])  
        #FALTA VALIDAR
        n_request.save()
        #print(r_form)
        #print(r_form['event_date'],r_form['init_hour'],r_form['finish_hour'])
        return redirect('requests_views')
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/new_client_e_request.html',data)

#New_info_request
def new_info_request(request):
    data = load_data_2()
    if request.method == 'POST':
        r_form = request.POST
        client = load_client(request.user)
        n_request = Info_request(petitioner=client,event_title=r_form['info_title'],status="Necesita revision",specification=r_form['info_detail'])  
        #FALTA VALIDAR
        n_request.save()
        #print(r_form)
        #print(r_form['event_date'],r_form['init_hour'],r_form['finish_hour'])
        return redirect('requests_views')
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/new_client_i_request.html',data)

#client_review_filter
def client_review(request,pk_id,r_type):
    if r_type == 0:
        return client_review_event(request,pk_id)
    elif r_type == 1:
        return client_review_info(request,pk_id)

#Client_review_request_event
def client_review_event(request,pk_id):
    object_request = Event_Request.objects.get(pk=pk_id)
    data = load_data_2(object_request)
    if request.method == 'POST':
        d_rcvd = request.POST
        if d_rcvd['estado']:
            object_request.status = d_rcvd['estado']
            object_request.save()
        else:
            pass
        return HttpResponse(pk_id)
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/client_review_event.html',data)

#Client_review_request_event
def client_review_info(request,pk_id):
    object_request = Info_request.objects.get(pk=pk_id)
    data = load_data_2(object_request)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/client_review_info.html',data)

#Client_modify_request
def modify_request(request,pk_id):
    object_request = Event_Request.objects.get(pk=pk_id)
    data = load_data_2(object_request)
    if request.method == 'POST':
        d_rcvd = request.POST
        print("cambiar datos")
        print(request.POST)
        print(type(object_request))
        object_request.modify_request(request.POST)
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/modify_request.html',data)

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::