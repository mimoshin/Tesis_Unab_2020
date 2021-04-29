from django.contrib.auth.models import AnonymousUser, User
from .models import User_Factory
from Solicitudes.models import Notify

#:::::::::::::::::::Functions:::::::::::::::::::::

def load_notify():
    all_notify = list(Notify.objects.filter(view=False))
    total = len(all_notify) 
    return(all_notify,total)

def load_data(Kwdata=None,**kwargs):
    u_notify = load_notify()
    data = {'u_notify':u_notify,'kwargs':Kwdata}
    if kwargs.get('athletes'):
        data['athletes'] = kwargs['athletes']
    return data
#:::::::::::::::::::::::::::::::::::::::::::::::::