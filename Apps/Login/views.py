from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser

#:::::::::::::::::::Functions:::::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::General_Views:::::::::::::::::

#Start_page
def start(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'start_page.html')

#Login
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

#Index_page
def index(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    return render(request,'login/index.html')
#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Admin_Views:::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Client_Views::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::


#:::::::::::::::::::Optional_Views::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::