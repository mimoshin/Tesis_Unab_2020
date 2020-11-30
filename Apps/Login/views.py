from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.decorators import login_required
from .models import User_Factory
from .utilities import load_data

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
        if user_auth:
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
    user_log = User_Factory.get_type_user(request.user)
    if user_log == 'admin':
        return admin_index(request)
    elif user_log == 'client':
        return client_index(request)
    return render(request,'login/index.html')

#Inscription_user_view | OPCIONAL-VERIFICAR SU USO 
def register(request):
    users = User_Factory.get_all_cient()
    if request.method == 'POST':
        print("POST: register ---- RECEPCIONANDO INSCRIPCIÓN")
        #User_Factory.register_client()
    if request.method == 'GET':
        pass
    return render(request,'login/register_user.html',{"users":Users})

#Modifiy_user_view | OPCIONAL-VERIFICAR SU USO 
def modify(request,pkid):
    #validar usuario
    selected_user = User_Factory(pkid)
    if request.method == 'POST':
        print("POST: modify ---- Modificando al usuario ",selected_user.first_name)
        if request.POST['first_name']:
            #selected_user.first_name = request.POST['first_name'] 
            pass
        if request.POST['last_name']:
            selected_user.last_name = request.POST['last_name']
            pass
        if request.POST['email']:
            selected_user.email = request.POST['email']
            pass
        #selected_user.save()
        #Validar formulario
        return redirect('admin_clients')
    if request.method == 'GET':
        pass
        print("GET: modify ---- selecionado el usuario ",selected_user.first_name)
    return render(request,'login/modify.html',{"user":selected_user})

#Delete_user_view | OPCIONAL-VERIFICAR SU USO 
def delete(request,pkid):
    selected_user = User_Factory.objects.get(pkid)
    print("elimnando al usuario")
    #selected_user.delete()
    print("eliminado")
    return redirect('/registrar')

#logout_view
def user_logout(request):
    logout(request)
    return redirect('/')
#:::::::::::::::::::::::::::::::::::::::::::::::::



#:::::::::::::::::::Admin_Views:::::::::::::::::::

#index_view
@login_required(login_url='/')
def admin_index(request):
    data = load_data()
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'base_admin.html',data)

#index_module_client_view
@login_required(login_url='/')
def admin_clients(request):
    users_list = User_Factory.get_all_cient()
    data = load_data(users_list)
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'login/admin_clients.html',data)

#Register_new_client_view
@login_required(login_url='/')
def new_client(request):
    data = load_data()
    if request.method == 'POST':
        data_request = request.POST
        result = User_Factory.register_client(data_request)
        if result:
            return redirect('admin_clients')
        else:
            return HttpResponse("Inscripcion fallida")
    if request.method == 'GET':
        pass
    return render(request,'login/new_client.html',data)

#Modify_client_view | modificando datos basicos del usuario
@login_required(login_url='/')
def modify_client(request,pk_id):
    dataclient = User_Factory.get_client(pk_id)
    selected_user = dataclient.log_user
    data = load_data(selected_user)
    if request.method == 'POST':
        data_form = request.POST
        #Validar formulario
        result = User_Factory.set_data_client(pk_id,data_form)
        if result:
            return redirect('admin_clients')
        else:
            pass
    if request.method == 'GET':
        pass
    return render(request,'login/modify_client.html',data)

#Delete_client_view
@login_required(login_url='/')
def delete_client(request,pk_id):
    if request.method == 'POST':
        #result = User_Factory.delete_client(pk_id)
        result = False
        if result:
            return redirect('admin_clients')
        else:
            return HttpResponse("No esta autorizado")
    if request.method == 'GET':
        pass
    return HttpResponse("No esta autorizado")
    

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::
@login_required(login_url='/')
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