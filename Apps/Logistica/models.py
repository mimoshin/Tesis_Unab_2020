from django.db import models

# Create your models here.
class event_calendar(models.Model):
    date = models.CharField(max_length=100,default="None") 
    event = models.CharField(max_length=100,default="None") 

    def __str__(self):
        return '{0}'.format(self.date)
    