from django.db import models
from django.utils import timezone
from Login.models import Client

# Create your models here.
class Event_Request(models.Model):
    petitioner = models.ForeignKey(Client,null=True,default="None",blank=True,on_delete=models.CASCADE)
    event_title = models.CharField(max_length=100,default="None") 
    event_type = models.CharField(max_length=100,default="None") 
    event_place = models.CharField(max_length=100,default="None") 
    event_date = models.CharField(max_length=100,default="None") 
    init_hour = models.CharField(max_length=100,default="None") 
    finish_hour = models.CharField(max_length=100,default="None") 
    text = models.CharField(max_length=100,default="None") 
    status = models.CharField(max_length=20,default="None") #Convertir en choices
    observation = models.CharField(max_length=500,default="None")    
    time_create = models.DateTimeField(auto_now=True,blank=True,null=True)  

    def __str__(self):
        return ("usuario: %s %s | estado: %s | creado:  %s "
                %(self.petitioner.client_person.first_name, self.petitioner.corp,
                self.status,self.time_create))
        
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

    def reviewed(self):
        if self.status == "Necesita revision":
            return False
        else:
            return True

class Info_request(models.Model):
    pass