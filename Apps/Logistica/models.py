from django.db import models
from Solicitudes.models import Event_Request

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