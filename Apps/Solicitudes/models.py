from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from Login.models import Client,Admin, User_Factory
from django.db.models.signals import pre_delete, pre_save , post_save, post_delete
from django.dispatch import Signal, receiver

#:::::Formats:::::
#Time --> HH-MM-SS
#Date --> YY-MM-DD
#Datetime --> YY-MM-DD / HH-MM-SS
#::::::::::::::::::

#::::Vars:::
STATUS = {'0':'Aprobado','1':'Rechazado','2':'Pendiente','3':'Respondida'}
Event_Choices = ((1,'Evento en general'),(2,'Torneo deportivo Individual'),(3,'Torneo deportivo por equipos'),(4,'otro tipo'))
Event_Zones = ((1,'Multicancha'),(2,'Pista Atlética'),(3,'Psicina'),(4,'Cancha Sintetica'),(5,'Gimnasio completo'),(6,'Lugar Externo'))
#:::::::::::::::


class IAbstract_request(models.Model):
    petitioner = models.ForeignKey(Client,blank=False,null=False,on_delete=models.CASCADE)
    event_title = models.CharField('Titulo de la solicitud',max_length=40,blank=False,null=False,default='event_title')
    status = models.CharField('Estado de la solicitud',max_length=20,blank=False,null=False,default='Necesita revision')
    specification = models.CharField('Especificación',max_length=100,blank=False,null=False,default='especification')     
    observation = models.CharField('Oberservaciones',max_length=300,blank=False,null=False,default='observation')    
    time_create = models.DateTimeField(auto_now=True,blank=False,null=False)
    class Meta:
        abstract = True

    def __str__(self):
        return "asbtract __str__"
    
    def get_type(self):
        return "abstract get_type"
    
    def get_status(self):
        return self.status
    
    def get_class(self) :
        return "abstract get_class"
    
    def set_status(self,new):
        self.status = STATUS[new]
        self.save()
    
    def set_request(self,args=None):
        return "Abstract set_request"
    
    def create_obs(self,observation):
        self.observation = observation
        self.save()

    def is_mod(self):
        actual_time = timezone.now()
        if self.reviewed():#¿Fue vista?
            return False #No modificable
        else:
            one_day = timezone.timedelta(days=1)
            #past_day = self.time_create - one_day
            #limit_time = past_day
            limit_time = self.time_create + one_day        
            if limit_time > actual_time:
                return True
            elif limit_time < actual_time:
                return False   
   
    
    def is_reviewed(self): #¿Fue revisada? 
        res = {'Necesita revision':False,'Pendiente':True}        
        try:return res[self.status]
        except:return True
    

class Event_request(IAbstract_request):
    event_type = models.IntegerField('Tipo de evento',choices=Event_Choices,blank=False,null=False,default=3)
    event_place = models.IntegerField('Lugar del evento',choices=Event_Zones,blank=False,null=False,default='6') 
    event_date = models.DateField('Fecha del evento',blank=False,null=False,default='2020-11-09') 
    init_hour = models.TimeField('Hora inicial',blank=False,null=False,default='08:00 a.m')
    finish_hour = models.TimeField('Hora Final',blank=False,null=False,default='09:00 a.m')    
    
    def __str__(self):
        return "Sol. n°{0} | Titulo {1} | estado: {2} ".format(self.pk,self.event_title,self.status)
    def get_type(self):
        return 'event'
    def get_class(self):
        return 'event_request'
    def set_request(self,args=None):
        if args.get('event_title'):
            self.event_title = args['event_title']
        if args.get('event_type'):
            self.event_type = args['event_type'] 
        if args.get('event_place'):
            self.event_place = args['event_place']
        if args.get('specification'):
            self.specification = args['specification'] 
        if args.get('event_date'):
            self.event_date = args['event_date'] 
        if args.get('init_hour'):
            self.init_hour = args['init_hour'] 
        if args.get('finish_hour'):
            self.finish_hour = args['finish_hour'] 
        self.save()


class Info_request(IAbstract_request):
    response = models.CharField('Respuesta',max_length=400,blank=False,null=False,default='response')
    
    def __str__(self):
        return "Sol. n°{0} | Titulo {1} |  estado: {2} ".format(self.pk,self.event_title,self.status)

    def get_type(self):
        return 'info'
    def get_class(self):
        return 'info_request'
    def set_response(self,response):
        self.response = response
        self.set_status('3')

    def set_request(self,args=None):
        if args.get('event_title'):
            self.event_title = args['event_title']
        if args.get('specification'):
            self.specification = args['specification'] 
        self.save()
        
class Request_Factory():
    @staticmethod
    def get_all(**kwargs):
        if kwargs.get('client'): #comprobar si recibo el parametro client
            first = list(Event_request.objects.filter(petitioner__log_user__pk=kwargs['client']))
            second = list(Info_request.objects.filter(petitioner__log_user__pk=kwargs['client']))
        else:
            first = list(Event_request.objects.all())
            second = list(Info_request.objects.all())
            
        for x in second:
            first.append(x)
        return first    
    @staticmethod
    def get_request(r_type,r_pk):
        """
        Get Object request
        """
        if r_type == 'event':
            r_object = Event_request.objects.get(pk=r_pk) #request object
            print("Retono event_request")
            return r_object
        elif r_type == 'info':
            r_object = Info_request.objects.get(pk=r_pk)
            return r_object
    @staticmethod
    def create_request(r_type,user_pk,data):
        if r_type == 'event':   
            time = data['event_date'].split('-')
            new_time = time[2]+'-'+time[1]+'-'+time[0]
            r_client = Client.objects.get(log_user__username=user_pk) #request client
            new_request = Event_request(petitioner=r_client,event_title=data['event_title'],event_type=data['event_type'],event_place=data['event_place'],
                                         specification=data['spe_ev'],event_date=new_time,init_hour=data['init_hour'],finish_hour=data['finish_hour'])  
        
        elif r_type == 'info':
            r_client = Client.objects.get(log_user__username=user_pk)
            new_request = Info_request(petitioner=r_client,event_title=data['info_title'],specification=data['info_detail'])  

        new_request.save()
        _notify_.send(sender=None,_class_=new_request.get_class(),_id_=new_request.pk)

    @staticmethod
    def set_estatus(_object_,_status_,user):
        r_class, r_id = _object_.get_class(), _object_.pk
        _object_.set_status(_status_)
        _notify_.send(sender=None,_class_=r_class,_id_=r_id,_view_=True)
        _viewer_.send(sender=None,_class_=r_class,_id_=r_id,_user_=user)
    @staticmethod
    def set_obs():
        pass
    @staticmethod
    def set_request(r_pk):
        pass
        

class IAbstract_notifys(models.Model):
    limit = models.Q(app_label='Solicitudes',model='event_request') | models.Q(app_label='Solicitudes',model='info_request')
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to=limit,blank=False,null=False)
    object_id = models.PositiveIntegerField(default=1,blank=False,null=False)
    content_object = GenericForeignKey('content_type', 'object_id')
    class Meta:
        abstract = True
    def __str__(self):
        return "Asbtract method __str__"

class Notify(IAbstract_notifys):
    view = models.BooleanField(default=False,blank=False,null=False)
    
    def __str__(self):
        if self.view:
            return "Solicitud N°: %s vista" % self.content_object.pk
        else:
            return "Notificar solicitud N° %s" % self.content_object.pk

class Viewer(IAbstract_notifys):
    name = models.CharField(max_length=200,blank=False,null=False)
    date = models.DateTimeField(default=False,null=False,blank=False)
    
    def __str__(self):
        return "El Usuario: %s ha visto la socilitud:  %s con fecha: %s " % (self.name,self.content_object.event_title,self.date)

class Notifys_Factory():
    @staticmethod
    def get_notify():
        pass
    def get_viewer():
        pass

            
#:::::::::::Signals::::::::::::::

_viewer_ = Signal(providing_args=['_class_','_id_','_user_'])

@receiver(_viewer_)
def view_signal(sender,**kwargs):
    print("Custom signal new_viewer")
    _class_, _id_ , user = kwargs.get('_class_'),kwargs.get('_id_'),kwargs.get('_user_')
    cont_type = ContentType.objects.get(app_label='Solicitudes', model=_class_) 
    new_viewer = Viewer(content_type=cont_type,object_id=_id_,name=user,date=timezone.now()) 
    new_viewer.save()
    object_notify = Notify.objects.get(content_type=cont_type,object_id=_id_)
    object_notify.view = True
    object_notify.save()
    
_notify_ = Signal(providing_args=['_class_','_id_'])

@receiver(_notify_)
def notify_signal(sender,**kwargs):
    print("creando notificacion")
    _class_,_id_= kwargs.get('_class_'),kwargs.get('_id_')
    cont_type = ContentType.objects.get(app_label='Solicitudes', model=_class_)
    if kwargs.get('_view_'):
        print("Custom signal view_notify")
        #object_notify = Notify.objects.get(content_type=cont_type,object_id=_id_) 
        #object_notify.view = True
        #object_notify.save()
    else:
        print("Custom signal new_notify")
        #new_notify = Notify(content_type=cont_type,object_id=_id_) 
        #new_notify.save()
    

def delete_notify(sender,instance,**kwargs):
    print('notify delete')
    _id_,_class_ = instance.pk, instance.get_class()
    cont_type = ContentType.objects.get(app_label='Solicitudes', model=_class_)
    #notify_del = Notify.objects.get(object_id=_id_,content_type=cont_type)
    #notify_del.delete()

def delete_viewer(sender,instance,**kwargs):
    print('viewer delete')
    _id_,_class_ = instance.pk, instance.get_class()
    cont_type = ContentType.objects.get(app_label='Solicitudes', model=_class_)
    #viewer_del = Viewer.objects.get(object_id=_id_,content_type=cont_type)
    #viewer_del.delete()

pre_delete.connect(delete_notify,sender=Info_request)
pre_delete.connect(delete_notify,sender=Event_request)
pre_delete.connect(delete_viewer,sender=Info_request)
pre_delete.connect(delete_viewer,sender=Event_request)


"""
def change_time(sender,instance,**kwargs):
    time = instance.event_date.split('-')
    new_time = time[2]+'-'+time[1]+'-'+time[0]
    instance.event_date = new_time
pre_save.connect(change_time,sender=Event_request)
"""