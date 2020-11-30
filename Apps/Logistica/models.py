from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from Solicitudes.models import Event_request,Request_Factory
from Login.models import Admin


# Create your models here.
class iEvent_calendar(models.Model):
    """
    El encargado de agendar eventos siempre sera un administrador de la corporación
    Dep_event: Evento dependiente de una solicitud.
    Ind_event: Evento independiente de una solicitud ( directo por la corporación )
    __attr__-->Event: GenericForeignKey para poder soportar almacenar los 3 tipos de eventos
    """
    creator = models.ForeignKey(Admin,blank=False,null=False,on_delete=models.CASCADE)
    limit = models.Q(app_label='Eventos',model='single_championship') | models.Q(app_label='Eventos',model='team_championship') | models.Q(app_label='Eventos',model='other_event')
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,default=1,limit_choices_to=limit)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')

    
    class Meta:
        abstract = True
    
    def __str__(self):
        return "Abstract Method __str__"
    def get_type(self):
        return "Abstract Method get_type"

class Dep_event(iEvent_calendar):
    e_request = models.ForeignKey(Event_request,default=None,blank=False,null=False,on_delete=models.CASCADE)
    
    def __str__(self):
        event = self.e_request.event_title
        date = self.e_request.event_date
        init = self.e_request.init_hour.strftime('%H')+':'+self.e_request.init_hour.strftime('%M')
        finish = self.e_request.finish_hour.strftime('%H')+':'+self.e_request.finish_hour.strftime('%M')

        return '{0} {1} {2} {3} {4}'.format(event,date,init,finish,self.content_object)

    def get_type(self):
        return "Dep"

class Ind_event(iEvent_calendar):
    """Event"""
    event_date = models.DateField(blank=False,null=False,default='2020-12-12')
    e_request = models.CharField(max_length=100,default="NoRequest") 
    specification = models.CharField(max_length=100,blank=False,null=False,default='especification')     
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
        new_filter = r'2020-12-.*'
        event_list = list(Dep_event.objects.filter(e_request__event_date__regex=month_filter))
        return event_list

    @staticmethod
    def ind_event(month,year):
        month_filter = r'{0}-{1}-.*'.format(str(year),str(month))
        event_list = list(Ind_event.objects.filter(event_date__regex = month_filter))
        return event_list
    @staticmethod
    def get_all(month,year):
        month_filter = r'{0}-{1}-.*'.format(str(year),str(month))
        Dep_list = list(Dep_event.objects.filter(e_request__event_date__regex=month_filter))
        Ind_list = list(Ind_event.objects.filter(event_date__regex = month_filter))
        for index in Ind_list:
            Dep_list.append(index)
        return Dep_list
    
    @staticmethod
    def get_all_day(filter_day):
        day_filter = r'{0}'.format(filter_day)
        Dep_list = list(Dep_event.objects.filter(e_request__event_date__regex=day_filter))
        Ind_list = list(Ind_event.objects.filter(event_date__regex = day_filter))
        for index in Ind_list:
            Dep_list.append(index)
        return Dep_list
    
    @staticmethod
    def get_client_events(client_pk,month,year):
        month_filter = r'{0}-{1}-.*'.format(str(year),str(month))
        Dep_list = list(Dep_event.objects.filter(e_request__event_date__regex=month_filter,e_request__petitioner__log_user__pk=client_pk))
        Ind_list = list(Ind_event.objects.filter(event_date__regex = month_filter))
        for index in Ind_list:
            Dep_list.append(index)
        return Dep_list
    
    @staticmethod
    def create_event(e_type,e_re,u_admin,event):
        if e_type == 'Ind':
            adm = Admin.objects.get(log_user__username=u_admn)        
            event = Dep_event(creator=adm,event='586',e_request=e_re) 
            event.save()
            
        elif e_type == 'Dep':
            admin =  Admin.objects.get(log_user__username=u_admin)         
            c_type = ContentType.objects.get(app_label='Eventos',model=event.get_class())
            new_event = Dep_event(creator=admin,e_request=e_re,content_type=c_type,object_id=event.pk) 
            new_event.save()
            





class project(models.Model):
    creator = models.ForeignKey(Admin,blank=False,null=False,on_delete=models.CASCADE,default=1)
    date_finish = models.DateField(blank=False,null=False,default='2020-12-12')
    date_init = models.DateField(blank=False,null=False,default='2020-12-12')
    details = models.CharField(max_length=300,blank=False,null=False,default='2020-12-12')
    project_title = models.CharField(max_length=60,blank=False,null=False,default='2020-12-12')
    status = models.CharField(max_length=20,blank=False,null=False,default='2020-12-12')