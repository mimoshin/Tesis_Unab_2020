from django.contrib.auth.models import AnonymousUser, User
from .models import User_Factory

#:::::::::::::::::::Functions:::::::::::::::::::::

def load_notify():
    notify_list = ["notificacion 1","notificacion 2","notificacion 3","notificacion 4","notificacion 5"]
    return notify_list

def load_data(Kwdata=None,**kwargs):
    u_notify = load_notify()
    data = {'u_notify':u_notify,'kwargs':Kwdata}
    if kwargs.get('athletes'):
        data['athletes'] = kwargs['athletes']
    return data
#:::::::::::::::::::::::::::::::::::::::::::::::::