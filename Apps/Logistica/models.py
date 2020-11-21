from django.db import models
from abc import abstractclassmethod,abstractstaticmethod,abstractmethod
from Solicitudes.models import Event_Request
from Login.models import Admin

# Create your models here.
class event_calendar(models.Model):
    date = models.CharField(max_length=100,default="None") 
    event = models.CharField(max_length=100,default="None") 

    def __str__(self):
        return '{0}'.format(self.date)
    
class other_event(models.Model):
    e_request = models.ForeignKey(Event_Request,default=None,blank=False,null=False,on_delete=models.CASCADE)
    def __str__(self):
        event = self.e_request.event_title
        date = self.e_request.event_date
        init = self.e_request.init_hour.strftime('%H')+':'+self.e_request.init_hour.strftime('%M')
        finish = self.e_request.finish_hour.strftime('%H')+':'+self.e_request.finish_hour.strftime('%M')

        return '{0} {1} {2} {3}'.format(event,date,init,finish)

    def date(self):
        date = self.e_request.event_date
        init = self.e_request.init_hour
        finish = self.e_request.finish_hour
        print(date,init,finish)




class iEvent_calendar(models.Model):
    """
    El encargado de agendar eventos siempre sera un administrador de la corporación
    Dep_event: Evento dependiente de una solicitud.
    Ind_event: Evento independiente de una solicitud ( directo por la corporación )
    """
    creator = models.ForeignKey(Admin,blank=False,null=False,on_delete=(models.CASCADE))
    event = models.CharField(max_length=100,default="None") 
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return "Abstract Method __str__"
    def get_type(self):
        return "Abstract Method get_type"

class Dep_event(iEvent_calendar):
    e_request = models.ForeignKey(Event_Request,default=None,blank=False,null=False,on_delete=models.CASCADE)
    
    def __str__(self):
        event = self.e_request.event_title
        date = self.e_request.event_date
        init = self.e_request.init_hour.strftime('%H')+':'+self.e_request.init_hour.strftime('%M')
        finish = self.e_request.finish_hour.strftime('%H')+':'+self.e_request.finish_hour.strftime('%M')

        return '{0} {1} {2} {3}'.format(event,date,init,finish)

    def get_type(self):
        return "Dep"

class Ind_event(iEvent_calendar):
    event_title = models.CharField(max_length=40,blank=False,null=False,default='event_title')
    event_type = models.CharField(max_length=15,blank=False,null=False,default='event_type')
    event_place = models.CharField(max_length=30,blank=False,null=False,default='event_place') 
    specification = models.CharField(max_length=100,blank=False,null=False,default='especification')     
    event_date = models.DateField(blank=False,null=False,default='2020-11-09') 
    init_hour = models.TimeField(blank=False,null=False,default='08:00 a.m')
    finish_hour = models.TimeField(blank=False,null=False,default='09:00 a.m')    
    e_request = models.CharField(max_length=100,default="NoRequest") 
    event_date = models.DateField(blank=False,null=False,default='2020-11-09')
    
    def __str__(self):
        event = self.event_title
        date = self.event_date
        init = self.init_hour.strftime('%H')
        finish = self.finish_hour.strftime('%H')
        return "{0} {1} {2} {3}".format(event,date,init,finish)
    
    def get_type(self):
        return "Ind"



class Calendar_Factory():
    @staticmethod
    def get_events(month,year):
        month_filter = r'{0}-{1}-.*'.format(str(year),str(month))
        event_list = list(Dep_event.objects.filter(e_request__event_date__regex=month_filter))
        return event_list

    @staticmethod
    def load_events(month,year):
        month_filter = r'{0}-{1}-.*'.format(str(year),str(month))
        event_list = list(other_event.objects.filter(e_request__event_date__regex = month_filter))
        return event_list

    @staticmethod
    def ind_event(month,year):
        month_filter = r'{0}-{1}-.*'.format(str(year),str(month))
        event_list = list(Ind_event.objects.filter(event_date__regex = month_filter))
        print(event_list)

    def get_all(month,year):
        month_filter = r'{0}-{1}-.*'.format(str(year),str(month))
        Dep_list = list(Dep_event.objects.filter(e_request__event_date__regex=month_filter))
        Ind_list = list(Ind_event.objects.filter(event_date__regex = month_filter))
        for index in Ind_list:
            Dep_list.append(index)
        return Dep_list




    