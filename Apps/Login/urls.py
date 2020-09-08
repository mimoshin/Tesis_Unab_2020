from django.urls import path
from . import views

urlpatterns =[
    path('',views.start,name='inicio'),
    path('ingreso',views.entry,name='ingreso'),
    path('index',views.index,name='index'),
    path('clientes',views.admin_clients,name='adm_clientes'),
    path('registrar',views.new_client,name='registrar_cliente'),
    path('modificar/<int:pk_id>',views.modify_client,name='modify_client'),
    path('eliminar/<int:pk_id>',views.delete_client,name='delete_client'),
    path('logout',views.user_logout,name='salir'),
    #Opcionales
    path('indexcliente',views.index_client,name='index_cliente'), #vista cliente directa
    path('indexadmin',views.index_admin,name='index_admin'),#vista administrador directa
    path('vista_registrar',views.register,name='registro'),#vista inicial
    path('vista_modificar/<int:pkid>',views.modify,name='modificar'),#vista inicial
    path('vista_eliminar/<int:pkid>',views.delete,name='eliminar'),#vista inicial
]   