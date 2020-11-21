from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.decorators import login_required
from .models import Admin, Client
from .utilities import type_user,load_data,load_notify

#:::::::::::::::::::Functions:::::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::General_Views:::::::::::::::::

#Start_page_view
def start(request):
    u_type = request.user
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        if u_type == AnonymousUser():
            u_type = 'anonimo'
        else:
            pass
    return render(request,'start_page.html',{'user':u_type})

#Login_view
def entry(request):
    if request.method == 'POST':
        username,password = request.POST['username'],request.POST['password']
        user_auth = authenticate(username=username,password=password)# T:User | F:None 
        if user_auth :
            login(request,user_auth)
            return redirect('index')
        else:
            messages.info(request, 'Usuario o contraseña incorrecto')

    if request.method == 'GET':
        if request.user == AnonymousUser():#usuario anonimo 
            return render(request,'login/login.html') 
        else: #usuario logeado
            return redirect('index') 

    logout(request)#terminar cualquier inicio de sesion
    return render(request,'login/login.html')

#Index_page_view
@login_required(login_url='/')
def index(request):
    user_log = type_user(request.user)
    if user_log == 'admin':
        return admin_index(request)
    elif user_log == 'client':
        return client_index(request)
    return render(request,'login/index.html')

#Inscription_user_view | OPCIONAL-VERIFICAR SU USO 
def register(request):
    Users = list(User.objects.all())
    if request.method == 'POST':
        print("POST: register ---- RECEPCIONANDO INSCRIPCIÓN")
        reg = User(username=request.POST["username"],first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],email=request.POST["email"])
        reg.set_password(request.POST["password"])
        reg.save()

    if request.method == 'GET':
        return render(request,'login/register_user.html',{"users_list":Users})
    return render(request,'login/register_user.html',{"users_list":Users})

#Modifiy_user_view | OPCIONAL-VERIFICAR SU USO 
def modify(request,pkid):
    #validar usuario
    selected_user = User.objects.get(pk=pkid)
    if request.method == 'POST':
        print("POST: modify ---- Modificando al usuario ",selected_user.first_name)
        if request.POST['first_name']:
            selected_user.first_name = request.POST['first_name'] 
        if request.POST['last_name']:
            selected_user.last_name = request.POST['last_name']
        if request.POST['email']:
            selected_user.email = request.POST['email']
        selected_user.save()
        #Validar formulario
        return redirect('admin_clients')
    if request.method == 'GET':
        print("GET: modify ---- selecionado el usuario ",selected_user.first_name)
        return render(request,'login/modify.html',{"user":selected_user})

    return render(request,'login/modify.html',{"user":selected_user})

#Delete_user_view | OPCIONAL-VERIFICAR SU USO 
def delete(request,pkid):
    selected_user = User.objects.get(pk=pkid)
    print("elimnando")
    selected_user.delete()
    print("eliminado")
    return redirect('/registrar')

#logout_view
def user_logout(request):
    logout(request)
    return redirect('/')
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Admin_Views:::::::::::::::::::

#index_view
def admin_index(request):
    data = load_data()
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'base_admin.html',data)

#index_module_client_view
def admin_clients(request):
    users_list = Client.objects.all()
    data = load_data(users_list)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'login/admin_clients.html',data)

#Register_new_client_view
def new_client(request):
    data = load_data()
    if request.method == 'POST':
        aux = request.POST
        new_user = User(username=aux['username'], first_name=aux['first_name'],last_name=aux['last_name'], email=aux['email'])
        new_user.set_password(aux["password"])
        new_user.save()
        new_client = Client(client_person=new_user, corp=aux['corp'], client_type=aux['type'])
        new_client.save()
        return redirect('admin_clients')
        
    if request.method == 'GET':
        return render(request,'login/new_client.html',data)
    return render(request,'login/new_client.html',data)

#Modify_client_view | modificando datos basicos del usuario
@login_required(login_url='/')
def modify_client(request,pk_id):
    aux_client = Client.objects.get(client_person__pk=pk_id)
    selected_user = aux_client.client_person
    data = load_data(selected_user)# reemplazo de load_data
    if request.method == 'POST':
        if request.POST['first_name']:
            selected_user.first_name = request.POST['first_name']
        if request.POST['last_name']:
            selected_user.last_name = request.POST['last_name']
            print("apellido",selected_user.last_name)
        if request.POST['email']:
            selected_user.email = request.POST['email']
        selected_user.save()
        #Validar formulario
        return redirect('admin_clients')
    if request.method == 'GET':
        return render(request,'login/modify_client.html',data)
    return render(request,'login/modify_client.html',data)

#Delete_client_view
def delete_client(request,pk_id):
    aux_client = Client.objects.get(client_person__pk=pk_id)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    print("quiero eliminar al usuario",aux_client)
    return redirect('admin_clients')

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::
def client_index(request):
    data = load_data(request.user)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'base_client.html',data)
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::