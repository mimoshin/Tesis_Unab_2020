from django.db import models
from abc import abstractclassmethod,abstractstaticmethod,abstractmethod
from Login.models import Client

Event_Choices = ((1,'Evento en general'),(2,'Torneo deportivo Individual'),(3,'Torneo deportivo por equipos'),(4,'otro tipo'))
Event_Zones = ((1,'Multicancha'),(2,'Pista Atlética'),(3,'Psicina'),(4,'Cancha Sintetica'),(5,'Gimnasio completo'),(6,'Lugar Externo'))

#:::::::Event factory:::::::::::::::::
class iEvent(models.Model):   
    organizer = models.ForeignKey(Client,blank=False,on_delete=models.CASCADE,default='1')
    event_title = models.CharField('Titulo del evento',max_length=40,blank=False,null=False,default='event_title')
    status = models.CharField('Estado',max_length=40,blank=False,null=False,default='Por realizar')
    observation = models.CharField('Oberservaciones',max_length=300,blank=False,null=False,default='observation')    
    event_type = models.IntegerField('Tipo de evento',choices=Event_Choices,blank=False,null=False,default=3)
    event_place = models.IntegerField('Lugar del evento',choices=Event_Zones,blank=False,null=False,default='6') 
    init_hour = models.TimeField('Hora inicial',blank=False,null=False,default='08:00 a.m')
    finish_hour = models.TimeField('Hora Final',blank=False,null=False,default='09:00 a.m')  
    event_date = models.DateField('Fecha del evento',blank=False,null=False,default='2020-11-09') 
    class Meta:
        abstract = True

    def __str__():
        return "Abstract method __str__"

    def get_type(self):
        return self.event_type
    def get_class():
        return "Abstract method get_class"

class Team_championship(iEvent):
    #CONVERTIRLOS EN INT
    max_teams = models.IntegerField('Cantidad maxima de equipos',default=10)
    ins_teams = models.IntegerField('Equipos inscritos',null=False,blank=False,default=0)
    def __str__(self):
        return "n° evento: {0} Torneo: {1} Tipo: {2} Numero de equipos: {3}".format(self.pk,self.event_title,self.event_type,self.max_teams)
    def get_class(self):
        return "team_championship"

class Single_championship(iEvent):
    max_athletes = models.IntegerField('Cantidad maxima de deportistas',default=50)
    ins_athletes = models.IntegerField('Deportistas inscritos',null=False,blank=False,default=0)
    def __str__(self):
        return "n° evento:{0} Torneo: {1} Tipo: {2} Numero de participantes: {3}".format(self.pk,self.event_title,self.event_type,self.max_athletes)
    def get_class(self):
        return "single_championship"

class Other_event(iEvent):
    max_person = models.IntegerField('Cantidad maxima de participantes',default=50)
    ins_person = models.IntegerField('Participantes inscritos',null=False,blank=False,default=0)
    def __str__(self):
        return "n° evento:{0} Torneo: {1} Tipo: {2} Numero de participantes: {3}".format(self.pk,self.event_title,self.event_type,self.max_person)
    def get_class(self):
        return "other_event"
    
class Event_factory():
    @staticmethod
    def create_event(**kwargs):
        #organizer | event_title | event_type | event_place | event_date | init_hour | finish_hour | status | observation 
        if kwargs: 
            data = kwargs['request'] 
            if data == 'NoRequest':
                data=kwargs['form']
                try:
                    if data['event_type'] == '1' or data['event_type'] == '4': #Other_event
                        new_event = Other_event(event_title=data['event_title'],event_type=data['event_type'],event_place=data['event_place'],
                                              event_date=data['event_date'],init_hour=data['init_hour'],finish_hour=data['finish_hour'])

                    elif data['event_type'] == '2': #Single_championship
                        new_event = Single_championship(event_title=data['event_title'],event_type=data['event_type'],event_place=data['event_place'],
                                              event_date=data['event_date'],init_hour=data['init_hour'],finish_hour=data['finish_hour'])
                
                    elif data['event_type'] == '3':
                        new_event = Team_championship(event_title=data['event_title'],event_type=data['event_type'],event_place=data['event_place'],
                                              event_date=data['event_date'],init_hour=data['init_hour'],finish_hour=data['finish_hour'])
                    
                except Exception as e:
                    print("error en no request")
                    print(e)

            else:
                if data.event_type == 1 or data.event_type == 4: #Other_event
                    new_event = Other_event(organizer=data.petitioner,event_title=data.event_title,event_type=data.event_type,event_place=data.event_place,
                                              event_date=data.event_date,init_hour=data.init_hour,finish_hour=data.finish_hour)

                elif data.event_type == 2: #Single_championship
                    new_event = Single_championship(organizer=data.petitioner,event_title=data.event_title,event_type=data.event_type,event_place=data.event_place,
                                                  event_date=data.event_date,init_hour=data.init_hour,finish_hour=data.finish_hour)
                
                elif data.event_type == 3:
                    new_event = Team_championship(organizer=data.petitioner,event_title=data.event_title,event_type=data.event_type,event_place=data.event_place,
                                              event_date=data.event_date,init_hour=data.init_hour,finish_hour=data.finish_hour)
            
        new_event.save()  
        return new_event

    @staticmethod
    def get_all():
        try:
            events,normal,other = list(Team_championship.objects.all()), list(Single_championship.objects.all()), list(Other_event.objects.all())
            for a in normal:
                events.append(a)
            for b in other:
                events.append(b)
            return events
        except:
            return 'nada'
    
    @staticmethod
    def get_event(e_type,e_id):
        event = False
        if e_type == 'team':
            if Team_championship.objects.filter(pk=e_id).exists():
                event = Team_championship.objects.get(pk=e_id)
        elif e_type == 'single':
            if Single_championship.objects.filter(pk=e_id).exists():
                event = Single_championship.objects.get(pk=e_id)
        elif e_type == 'other':
            if  Other_event.objects.filter(pk=e_id).exists():
                event = Other_event.objects.get(pk=e_id)
        
        if event:
            return event
        else:
            return []

    @staticmethod
    def get_my_events(pk):
        try:
            events,normal,other = list(Team_championship.objects.filter(organizer__log_user__pk=pk)), list(Single_championship.objects.filter(organizer__log_user__pk=pk)), list(Other_event.objects.filter(organizer__log_user__pk=pk))            
            for a in normal:
                events.append(a)
            for b in other:
                events.append(b)
            return events
        except:
            return 'nada'
    @staticmethod
    def set_observation(data,**kwargs):
        if kwargs:
            event = kwargs['event']
            event.observation = data
            event.save()
        else:
            print("buscar el evento para agregarle una observacion")

#:::::::End event factory:::::::::::::

class Team(models.Model):
    event = models.ForeignKey(Team_championship,blank=False,null=False,on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=40,blank=False,null=False,default='Equipo_Random',unique=True)
    max_atheteles = models.IntegerField(blank=False,null=False,default=10)
    max_reserve = models.IntegerField(blank=False,null=False,default=10)
    athletes = models.IntegerField(blank=False,null=False,default=0)
    reserve = models.IntegerField(blank=False,null=False,default=0)

    def __str__(self):
        name,num,pk = self.name,self.max_atheteles,self.pk
        return "pk_team {0} Equipo {1} n° participantes: {2}".format(pk,name,num)
    
    

class Team_Factory():
    @staticmethod
    def create_team(**kwargs):
        try:
            data = kwargs['data']
            new_team = Team(name=data['team_name'],max_atheteles=8,event=kwargs['event'])
            new_team.save()
        except:
            print("algo fallo en la inscripcion del equipo")
    @staticmethod
    def get_event_teams(id_event):
        Qteams = list(Team.objects.filter(event=id_event).values())
        return Qteams
    @staticmethod
    def get_team(id_team):
        Qteam = Team.objects.get(pk=id_team)
        return Qteam
    @staticmethod
    def set_max(id_team,p_type):
        Qteam = Team.objects.get(pk=id_team)
        if p_type == 'Reserva':
            Qteam.reserve+=1
        elif p_type == 'Titular':
            Qteam.athletes+=1
        Qteam.save()


#:::::::athlete factory:::::::::::::
class iPerson(models.Model):
    first_name = models.CharField('Nombre',max_length=40,blank=False,null=False,default='Nombre')
    last_name = models.CharField('Apellido',max_length=40,blank=False,null=False,default='Apellido')
    age = models.IntegerField(blank=False,null=False,default=20)
    email = models.CharField(max_length=40,blank=False,null=False,default='hola@hola.com')
    status = models.CharField(max_length=40,blank=False,null=False,default='Inscrito')
    class Meta:
        abstract = True 
    
    def __str__(self):
        return "Abstract method __str__"

class Athlete(iPerson):
    event = models.ForeignKey(Single_championship,blank=False,null=False,on_delete=models.CASCADE,default=1)
    results = models.CharField(max_length=40,blank=False,null=False,default='noWin')
    club = models.CharField(max_length=40,blank=False,null=False,default='Cerro Navia')
    
class Athlete_team(iPerson):
    position = models.CharField(max_length=7,blank=False,null=False,default='Titular')
    my_team = models.ForeignKey(Team,blank=False,null=False,on_delete=models.CASCADE,default=1)
    
    def __str__(self):
        return "Deportista: %s %s | Edad: %s | Equipo: %s" % (self.first_name,self.last_name,self.age,self.team)

class Other_person(iPerson):
    event = models.ForeignKey(Other_event,blank=False,null=False,on_delete=models.CASCADE,default=1)

class Athlete_factory():
    @staticmethod
    def get_athletes(**kwargs):
        if kwargs:
            if kwargs['type'] == 'single':    
                e_id = kwargs['id_event']
                data = Athlete.objects.filter(event=e_id).values()
            elif kwargs['type'] == 'team':
                t_id = kwargs['team']
                data = Athlete_team.objects.filter(my_team=t_id).values()
            elif kwargs['type'] == 'other':
                e_id = kwargs['event']
                data = Other_person.objects.filter(event=e_id).values()
            return list(data)
        else:
            print("no pasa nada")
   
    @staticmethod
    def create_athlete(**kwargs):
        if kwargs:
            data = kwargs.get('form')
            try:
                if kwargs['type'] == 'single':
                    # first_name | last_name | age | email | status | results | event | club     
                    new_athlete = Athlete(  first_name=data['first_name'],last_name=data['last_name'],age=data['age'],
                                            email=data['email'],event=kwargs['event'],club=data['club'])
                elif kwargs['type'] == 'team':
                    # first_name | last_name | age | email | status | event | team | position 
                    new_athlete = Athlete_team( first_name=data['first_name'],last_name=data['last_name'],age=data['age'],
                                                email=data['email'],my_team=kwargs['team'],position=data['position'])
                elif kwargs['type'] == 'other':
                    # first_name | last_name | age | email | status | event 
                    new_athlete = Other_person( first_name=data['first_name'],last_name=data['last_name'],age=data['age'],
                                                email=data['email'],event=kwargs['event'])
                new_athlete.save()
            except Exception as e:
                print("Problemas al inscribir un deportista")
                print(e)
                





    