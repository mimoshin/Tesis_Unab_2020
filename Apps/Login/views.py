from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User

#:::::::::::::::::::Functions:::::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::General_Views:::::::::::::::::

#Start_page
def start(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    aux = str(request.user)
    print(aux)
    return render(request,'start_page.html')

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
def index(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'login/index.html')

#Inscription_user_view
def register(request):
    Users = list(User.objects.all())
    if request.method == 'POST':
        print("POST: register ---- RECEPCIONANDO INSCRIPCIÓN")
        b = User(username=request.POST["username"],first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],email=request.POST["email"])
        b.set_password(request.POST["password"])
        b.save()

    if request.method == 'GET':
        return render(request,'login/register.html',{"users_list":Users})
    return render(request,'login/register.html',{"users_list":Users})

#Modifiy_user_view
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
        return redirect('index')
    if request.method == 'GET':
        print("GET: modify ---- selecionado el usuario ",selected_user.first_name)
        return render(request,'login/modify.html',{"user":selected_user})

    return render(request,'login/modify.html',{"user":selected_user})

#Delete_user_view
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

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::