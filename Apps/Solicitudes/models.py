from django.db import models
from django.utils import timezone
from datetime import datetime
from Login.models import Client
from abc import abstractclassmethod,abstractstaticmethod,abstractmethod


#:::::Formats:::::
#Time --> HH-MM-SS
#Date --> YY-MM-DD
#Datetime --> YY-MM-DD / HH-MM-SS
#::::::::::::::::::

#::::Constant:::
STATUS = {'0':'Aprobado','1':'Rechazado','2':'Pendiente','3':'Respondida'}
#:::::::::::::::

# Create your models here.
class Event_Request(models.Model):
    petitioner = models.ForeignKey(Client,blank=False,null=False,on_delete=models.CASCADE)
    event_title = models.CharField(max_length=40,blank=False,null=False,default='event_title')
    event_type = models.CharField(max_length=15,blank=False,null=False,default='event_type')
    event_place = models.CharField(max_length=30,blank=False,null=False,default='event_place') 
    status = models.CharField(max_length=20,blank=False,null=False,default='status')
    specification = models.CharField(max_length=100,blank=False,null=False,default='especification')     
    observation = models.CharField(max_length=300,blank=False,null=False,default='observation')    
    event_date = models.DateField(blank=False,null=False,default='2020-11-09') 
    init_hour = models.TimeField(blank=False,null=False,default='08:00 a.m')
    finish_hour = models.TimeField(blank=False,null=False,default='09:00 a.m')    
    time_create = models.DateTimeField(auto_now=True,blank=False,null=False)
    #active = models.BooleanField(blank=False,null=False,default=True)

    def __str__(self):
        button = self.modify_button()
        return "Sol. n°{0} | Titulo {1} | tipo: {2} | estado: {3} | creado:  {4}".format(self.pk,self.event_title,self.event_type,self.status,button)
        
    def modify_button(self):
        actual_time = timezone.now()
        if self.reviewed():
            return False
        else:
            one_day = timezone.timedelta(days=1)
            #past_day = self.time_create - one_day
            #limit_time = past_day
            limit_time = self.time_create + one_day        
            if limit_time > actual_time:
                return True
            elif limit_time < actual_time:
                return False    

    def reviewed(self): #¿Fue revisada? 
        if self.status == "Necesita revision":
            return False
        elif self.status == 'Pendiente':
            return True
        else:
            return True
    
    def modify_request(self,args=None):
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
        print(args['init_hour'])
        self.save()

    def create_obs(self,observation):
        self.observation = observation
        self.save()
    
    def set_status(self,status):
        self.status = STATUS[status]
        print("recibiendo status: ", STATUS[status])
        self.save()
    
    def get_type(self):
        return 'event'
    
    def get_month(self):
        return 'hola'

    def get_day(self):
        print(self.event_date)
        

class Info_request(models.Model):
    petitioner = models.ForeignKey(Client,blank=False,null=False,on_delete=models.CASCADE,default=None)
    event_title = models.CharField(max_length=40,blank=False,null=False,default='event_title')
    status = models.CharField(max_length=20,blank=False,null=False,default='status')
    specification = models.CharField(max_length=100,blank=False,null=False,default='especification')     
    observation = models.CharField(max_length=300,blank=False,null=False,default='observation')    
    time_create = models.DateTimeField(auto_now=True,blank=False,null=False)
    response = models.CharField(max_length=400,blank=False,null=False,default='response')
    #active = models.BooleanField(blank=False,null=False,default=True)

    def __str__(self):
        button = self.modify_button()
        return "Sol. n°{0} | Titulo {1} | estado: {2} | creado:  {3}".format(self.pk,self.event_title,self.status,button)

    def create_obs(self,observation):
        self.observation = observation
        self.save()

    def set_response(self,response):
        self.response = response
        self.set_status('3')

    def set_status(self,status):
        self.status = STATUS[status]
        self.save()
        
    def modify_button(self):
        actual_time = timezone.now()
        if self.reviewed():
            return False
        else:
            one_day = timezone.timedelta(days=1)
            #past_day = self.time_create - one_day
            #limit_time = past_day
            limit_time = self.time_create + one_day        
            if limit_time > actual_time:
                return True
            elif limit_time < actual_time:
                return False    

    def reviewed(self):#¿Fue revisada? 
        if self.status == "Necesita revision":
            return False
        elif self.status == 'Pendiente':
            return True
        else:
            return True
    
    def get_type(self):
        return 'info'


"""
class IAbstract_request(models.Model):
    #petitioner = models.ForeignKey('Solicitante',Client,blank=False,null=False,on_delete=models.CASCADE,default=None)
    #event_title = models.CharField('Titulo de la solicitud',max_length=40,blank=False,null=False,default='event_title')
    #status = models.CharField('Estado de la solicitud',max_length=20,blank=False,null=False,default='status')
    #specification = models.CharField('Especificación',max_length=100,blank=False,null=False,default='especification')     
    #observation = models.CharField('Oberservaciones',max_length=300,blank=False,null=False,default='observation')    
    #time_create = models.DateTimeField(auto_now=True,blank=False,null=False)
    @abstractmethod
    def __str__(self):
        return "asbtract __str__"
    @abstractmethod
    def get_type(self):
        return "abstract get_type"
    @abstractmethod
    def get_status(self):
        return self.status
    @abstractmethod
    def set_status(self,new):
        self.status = STATUS[new]
        self.save()
    @abstractmethod
    def set_request(self,args=None):
        return "Abstract set_request"
    @abstractmethod
    def create_obs(self,observation):
        self.observation = observation
        self.save()

    @abstractmethod
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
    @abstractmethod
    def is_reviewed(self): #¿Fue revisada? 
        res = {'Necesita revision':False,'Pendiente':True}        
        try:
            return res[self.status]
        except:
            return True
    

class sEvent_request(IAbstract_request):
    #event_type = models.CharField('Tipo de evento',max_length=15,blank=False,null=False,default='event_type')
    #event_place = models.CharField('Lugar del evento',max_length=30,blank=False,null=False,default='event_place') 
    #event_date = models.DateField('Fecha del evento',blank=False,null=False,default='2020-11-09') 
    #init_hour = models.TimeField('Hora inicial',blank=False,null=False,default='08:00 a.m')
    #finish_hour = models.TimeField('Hora Final',blank=False,null=False,default='09:00 a.m')    
    pass
    
    def __str__(self):
        button = self.modify_button()
        return "Sol. n°{0} | Titulo {1} | estado: {2} | creado:  {3}".format(self.pk,self.event_title,self.status,button)
        
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
        print(args['init_hour'])
        self.save()
    
class sInfo_request(IAbstract_request):
    #response = models.CharField('Respuesta',max_length=400,blank=False,null=False,default='response')
    pass
    def __str__(self):
        button = self.modify_button()
        return "Sol. n°{0} | Titulo {1} | tipo: {2} | estado: {3} | creado:  {4}".format(self.pk,self.event_title,self.event_type,self.status,button)
        
    def set_response(self,response):
        self.response = response
        self.set_status('3')

    def set_request(self,args=None):
        if args.get('event_title'):
            self.event_title = args['event_title']
        if args.get('specification'):
            self.specification = args['specification'] 
        print(args)
        self.save()
        
class Request_Factory():
    @staticmethod
    def get_request():
        pass
    @staticmethod
    def total_requests():
        pass
    
"""
