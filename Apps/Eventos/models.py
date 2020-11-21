from django.db import models
from abc import abstractclassmethod,abstractstaticmethod,abstractmethod
from Login.models import Client

#:::::::Event factory:::::::::::::::::
class iEvent(models.Model):   
    organizer = models.ForeignKey(Client,blank=False,on_delete=models.CASCADE,default=2)
    event_title = models.CharField(max_length=40,blank=False,null=False,default='event_title')
    event_type = models.CharField(max_length=40,blank=False,null=False,default='event_title')
    status = models.CharField(max_length=40,blank=False,null=False,default='Por realizar')
    @abstractstaticmethod
    def __str__():
        return """Event description function"""
    @abstractmethod
    def get_type(self):
        return self.event_type

class Team_championship(iEvent):
    max_teams =  models.CharField(max_length=40,blank=False,null=False,default='10')
    def __str__(self):
        return "n° evento: {0} Torneo: {1} Tipo: {2} Numero de equipos: {3}".format(self.pk,self.event_title,self.event_type,self.max_teams)

class Single_championship(iEvent):
    max_athletes = models.IntegerField(default=1)
    def __str__(self):
        return "n° evento:{0} Torneo: {1} Tipo: {2} Numero de participantes: {3}".format(self.pk,self.event_title,self.event_type,self.max_athletes)

class Other_event(iEvent):
    max_person = models.IntegerField(default=1)
    def __str__(self):
        return "n° evento:{0} Torneo: {1} Tipo: {2} Numero de participantes: {3}".format(self.pk,self.event_title,self.event_type,self.max_person)
    
class Event_factory():
    @staticmethod
    def create_event(event_type,data=None):
        try:
            if event_type == 'team_championship':
                if data:
                    return Team_championship(event_type='torneo por equipos')
                else:
                    return Team_championship(event_type='torneo por equipos')
            elif event_type == 'single_championship':
                if data:
                    return Single_championship(event_type='torneo individual')
                else:
                    return Single_championship(event_type='torneo individual')
            elif event_type == 'other_event':
                if data:
                    return Other_event(event_type='otro evento')
                else:
                    return Other_event(event_type='otro evento')

        except AssertionError as e:
            print(e)

    @staticmethod
    def get_all():
        events,normal,other = list(Team_championship.objects.all()), list(Single_championship.objects.all()), list(Other_event.objects.all())
        for a in normal:
            events.append(a)
        for b in other:
            events.append(b)
        return events
    
    @staticmethod
    def get_event(e_type,e_id):
        if e_type == 'team':
            return Team_championship.objects.get(pk=e_id)
        elif e_type == 'single':
            return Single_championship.objects.get(pk=e_id)
        elif e_type == 'other':
            return Other_event.objects.get(pk=e_id)

    @staticmethod
    def my_events(pk_club):
        pass

    @staticmethod
    def find(pk):
        pass

#:::::::End event factory:::::::::::::

#:::::::athlete factory:::::::::::::
class iPerson(models.Model):
    first_name = models.CharField('Nombre',max_length=40,blank=False,null=False,default='Franco')
    last_name = models.CharField('Apellido',max_length=40,blank=False,null=False,default='Vega')
    age = models.CharField(max_length=40,blank=False,null=False,default='24')
    email = models.CharField(max_length=40,blank=False,null=False,default='hola@hola.com')
    status = models.CharField(max_length=40,blank=False,null=False,default='noActive')
    @abstractclassmethod
    def __str__(self):
        return "hola este es el metodo abstracto"

class athlete(iPerson):
    results = models.CharField(max_length=40,blank=False,null=False,default='noWin')
    event = models.IntegerField(default=0)
    club = models.CharField(max_length=40,blank=False,null=False,default='Cerro Navia')
    
class athlete_team(iPerson):
    team = models.CharField(max_length=40,blank=False,null=False,default='noTeam')

class other_person(iPerson):
    event = models.IntegerField(default=0)

class Athlete_factory():
    @staticmethod
    def get_athlete_event(a_type,e_id):
        if a_type == 'single':
            data = athlete.objects.filter(event=e_id).values()
            return list(data)
        elif a_type == 'team':
            data = athlete_team.objects.filter(event=e_id).values()
            return list(data)
        elif a_type == 'other':
            data = other_person.objects.filter(event=e_id).values()
            return list(data)

class team(models.Model):
    name = models.CharField(max_length=40,blank=False,null=False,default='team_name')
    total_atheteles = models.CharField(max_length=40,blank=False,null=False,default='total_ins')
    event = models.IntegerField(default=0)

    def __str__(self):
        name,num,pk = self.name,self.total_atheteles,self.pk
        return "pk_team {0} Equipo {1} n° participantes: {2}".format(pk,name,num)

class project(models.Model):
    project_title = models.CharField(max_length=40,blank=False,null=False,default='event_title')
    project_type = models.CharField(max_length=15,blank=False,null=False,default='event_type')
    status = models.CharField(max_length=20,blank=False,null=False,default='status')
    specification = models.CharField(max_length=100,blank=False,null=False,default='especification')     
    observation = models.CharField(max_length=300,blank=False,null=False,default='observation')
    init_date = models.DateField(blank=False,null=False,default='2020-11-09')
    finish_date = models.DateField(blank=False,null=False,default='2020-11-09')
    