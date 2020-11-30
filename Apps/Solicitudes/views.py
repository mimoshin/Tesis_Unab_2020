from django.shortcuts import render, redirect, HttpResponse
from .models import Request_Factory
from .forms import pruebaForm, otroForm
from Login.models import User_Factory
from Login.utilities import load_notify,load_data

#:::::::::::::::::::Functions:::::::::::::::::::::
def load_client(user):
    client = Client.objects.get(client_person=user)
    return client
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::General_Views:::::::::::::::::
#Index_equests_view
def requests_view(request):
    user_log = User_Factory.get_type_user(request.user)
    if user_log == 'admin':
        return admin_requests(request)
    elif user_log == 'client':
        return client_requests(request)
    return redirect('/')
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Admin_Views:::::::::::::::::::
#Admin_requests_view
def admin_requests(request):
    requests_list = Request_Factory.get_all()
    data = load_data(requests_list)
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
    object_request = Request_Factory.get_request('event',pk_id)
    data = load_data(object_request)
    if request.method == 'POST':
        d_rcvd = request.POST
        stat_obs = d_rcvd.get('estado'),d_rcvd.get('observation')
        if stat_obs[0]:
            object_request.set_status(stat_obs[0])
        elif stat_obs[1]:
            object_request.create_obs(stat_obs[1])
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/admin_review_event.html',data)

#Admin_review_request_info
def review_request_info(request,pk_id):
    object_request = Request_Factory.get_request('info',pk_id)
    data = load_data(object_request)
    if request.method == 'POST':
        d_rcvd = request.POST
        response = d_rcvd.get('response')
        stat_obs = d_rcvd.get('estado'),d_rcvd.get('observation')
        if stat_obs[0]:
            object_request.set_status(stat_obs[0])
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
    requests_list = Request_Factory.get_all(client=pk)
    #requests_list = total_requests(client=pk)
    data = load_data(requests_list)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/client_requests.html',data)

#New_event_request
def new_event_request(request):
    data = load_data()
    if request.method == 'POST':
        r_form = request.POST
        Request_Factory.create_request('event',request.user,r_form)
        return redirect('requests_views')
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/new_client_e_request.html',data)

#New_info_request
def new_info_request(request):
    data = load_data()
    if request.method == 'POST':
        r_form = request.POST
        Request_Factory.create_request('info',request.user,r_form)
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
    object_request = Request_Factory.get_request('event',pk_id)
    data = load_data(object_request)
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
    object_request = Request_Factory.get_request('info',pk_id)
    data = load_data(object_request)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'Solicitudes/client_review_info.html',data)

#Client_modify_request
def modify_request(request,r_type,pk_id):
    templates = {'event':'Solicitudes/modify_request.html','info':'Solicitudes/modify_info_request.html'}
    object_request = Request_Factory.get_request(r_type,pk_id)
    data = load_data(object_request)
    if request.method == 'POST':
        print('hola')
        print(request.path)
        print(request.POST)
        #d_rcvd = request.POST
        #print("cambiar datos")
        #print(request.POST)
        #print(type(object_request))
        #object_request.modify_request(request.POST)ss
    if request.method == 'GET':
        pass
    return render(request,templates[r_type],data)

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::