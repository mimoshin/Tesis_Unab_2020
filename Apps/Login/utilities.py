from django.contrib.auth.models import AnonymousUser, User
from .models import Admin, Client

#:::::::::::::::::::Functions:::::::::::::::::::::
def type_user(r_user):
    admin = Admin.objects.filter(admin_person__username = r_user).exists()
    client = Client.objects.filter( client_person__username = r_user).exists()
    if admin:
        return 'admin'
    elif client:
        return 'client'

def load_notify():
    notify_list = ["notificacion 1","notificacion 2","notificacion 3","notificacion 4","notificacion 5"]
    return notify_list

def load_data(kwargs = None):
    u_notify = load_notify()
    data = {'u_notify':u_notify,'kwargs':kwargs}
    return data
#:::::::::::::::::::::::::::::::::::::::::::::::::