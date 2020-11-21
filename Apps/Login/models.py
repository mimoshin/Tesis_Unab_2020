from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class Admin(models.Model):
    admin_person = models.ForeignKey(User,blank=False,on_delete=models.CASCADE)
    #Otros datos por definir

    def __str__(self):
        return ("Administrador: {0} {1}".format(self.admin_person.first_name,self.admin_person.last_name))
    

class Client(models.Model):
    client_person = models.ForeignKey(User,blank=False,on_delete=models.CASCADE)
    corp = models.CharField(max_length=20,blank=True,null=True,default=None)
    #Convertir client_type en choiches
    client_type = models.CharField(max_length=20,blank=True,null=True,default=None)    
    #Otros datos por definir

    def __str__(self):
        return ("Cliente: {0} | Institución {1} | tipo: {2}".format(self.client_person.first_name,self.corp,self.client_type))

