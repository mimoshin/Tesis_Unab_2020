from django.db import models
from django.utils import timezone
from datetime import datetime
from Login.models import Client,Admin



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
        if r_type == 'event':
            r_object = Event_request.objects.get(pk=r_pk) #request object
            return r_object
        elif r_type == 'info':
            r_object = Info_request.objects.get(pk=r_pk)
            return r_object
    @staticmethod
    def create_request(r_type,user_pk,data):
        if r_type == 'event':   
            r_client = Client.objects.get(log_user__username=user_pk) #request client
            print(data)
            new_request = Event_request(petitioner=r_client,event_title=data['event_title'],event_type=data['event_type'],event_place=data['event_place'],
                                         specification=data['spe_ev'],event_date=data['event_date'],init_hour=data['init_hour'],finish_hour=data['finish_hour'])  
        
            new_request.save()

        elif r_type == 'info':
            r_client = Client.objects.get(log_user__username=user_pk)
            new_request = Info_request(petitioner=r_client,event_title=data['info_title'],specification=data['info_detail'])  
            new_request.save()
    @staticmethod
    def set_estatus(r_type,r_pk):
        pass
    @staticmethod
    def set_obs():
        pass
    @staticmethod
    def set_request(r_pk):
        pass
        
