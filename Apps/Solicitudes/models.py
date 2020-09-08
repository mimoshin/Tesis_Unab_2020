from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Event_Request(models.Model):
    petitioner = models.ForeignKey(User,null=True,default="None",blank=True,on_delete=models.CASCADE)
    text = models.CharField(max_length=100) 
    status = models.CharField(max_length=20) #Convertir en choices
    observation = models.CharField(max_length=500)    
    time_create = models.DateTimeField(auto_now=True,blank=True,null=True)  

    def __str__(self):
        return "usuario: {0}, estado: {1} creado: {2}".format(self.petitioner.first_name,self.status,self.time_create)
        
    def modify_button(self):
        if self.reviewed():
            return False
        else:
            one_day = timezone.timedelta(days=1)
            #past_day = self.time_create - one_day
            #limit_time = past_day
            limit_time = self.time_create + one_day        
            if limit_time > self.time_create:
                return True
            elif limit_time < self.time_create:
                return False    

    def reviewed(self):
        if self.status == "Necesita revision":
            return False
        else:
            return True