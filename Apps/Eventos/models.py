from django.db.models.signals import pre_delete, pre_save , post_save, post_delete
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from Login.models import User_Factory


"""
    ::::::::::::::::: Modulo que permite la creacion de eventos :::::::::::::::::

    Pemite crear 3 tipos de eventos: 
        *** Un evento siempre debe tener un organizador: Administrador o cliente ***

        Torneo deportivo Individual (EJ: Pin-Pong, Karate, etc)
        Torneo deportivo por Equipos (EJ: Futbol, Voleiball, etc)
        Otro tipo de Evento (Zumba, taller deportivo, etc)
"""

Event_Choices = ((1,'Evento en general'),(2,'Torneo deportivo individual'),(3,'Torneo deportivo por equipos'),(4,'Otro tipo de evento'))
Event_Zones = ((1,'Multicancha'),(2,'Pista Atlética'),(3,'Psicina'),(4,'Cancha Sintetica'),(5,'Gimnasio completo'),(6,'Lugar externo'))
Status_Choices = ((1,'Por realizar'),(2,'Iniciado'),(3,'Finalizado'),(4,'Suspendido'))

#:::::::Event factory:::::::::::::::::
class iEvent(models.Model):
    #organizer = models.ForeignKey(Client,blank=False,on_delete=models.CASCADE,default='4')
    #status = models.CharField('Estado',max_length=40,blank=False,null=False,default='Por realizar')
    limit = models.Q(app_label='Login',model='client') | models.Q(app_label='Login',model='admin')
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,default=1,limit_choices_to=limit)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')
    event_title = models.CharField('Titulo del evento',max_length=40,blank=False,null=False,default='event_title')
    status = models.IntegerField('Estado',choices=Status_Choices,blank=False,null=False,default=1)
    observation = models.CharField('Oberservaciones',max_length=300,blank=False,null=False,default='observation')    
    event_type = models.IntegerField('Tipo de evento',choices=Event_Choices,blank=False,null=False,default=3)
    event_place = models.IntegerField('Lugar del evento',choices=Event_Zones,blank=False,null=False,default=6) 
    init_hour = models.TimeField('Hora inicial',blank=False,null=False,default='08:01:00')
    finish_hour = models.TimeField('Hora Final',blank=False,null=False,default='09:01:00')  
    event_date = models.DateField('Fecha del evento',blank=False,null=False,default='2020-11-09') 
    class Meta:
        abstract = True

    def __str__(self):
        return "Abstract method __str__"

    def get_type(self):
        return self.event_type
    def get_class(self):
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
        return "n° evento:{0} Torneo: {1} Tipo: {2} Numero de participantes: {3}".format(self.content_object,self.event_title,self.event_type,self.max_athletes)
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
        """
        organizer(Contentype & object_id) | event_title | event_type | event_place | event_date | init_hour | finish_hour | status | observation 
        Crea un evento primeramente filtrando por organizador (cliente o administrador)
        """
        if kwargs: 
            if kwargs.get('organizer'):
                if kwargs['organizer'] == 'client':
                    data = kwargs['request'].__dict__
                    _id_ = data['petitioner_id']
                    cont_type = ContentType.objects.get(app_label='Login', model='client') 
                 
                elif kwargs['organizer'] == 'admin':
                    _id_ = kwargs['user']
                    cont_type = ContentType.objects.get(app_label='Login', model='admin') 
                    data = kwargs['form']

                try:    
                    if int(data['event_type']) == 1 or int(data['event_type']) == 4: #Other_event
                        new_event = Other_event(content_type=cont_type,object_id=_id_,event_title=data['event_title'],event_type=data['event_type'],event_place=data['event_place'],
                                              event_date=data['event_date'],init_hour=data['init_hour'],finish_hour=data['finish_hour'])

                    elif int(data['event_type']) == 2: #Single_championship
                        new_event = Single_championship(content_type=cont_type,object_id=_id_,event_title=data['event_title'],event_type=data['event_type'],event_place=data['event_place'],
                                              event_date=data['event_date'],init_hour=data['init_hour'],finish_hour=data['finish_hour'])
                
                    elif int(data['event_type']) == 3:
                        new_event = Team_championship(content_type=cont_type,object_id=_id_,event_title=data['event_title'],event_type=data['event_type'],event_place=data['event_place'],
                                              event_date=data['event_date'],init_hour=data['init_hour'],finish_hour=data['finish_hour'])
                    print("Evento Creado")
                    new_event.save()  
                    return new_event

                except Exception as e:
                    print("Error en la creación del evento ---> Error en concreto:",e)

                
    
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
        client = User_Factory.get_client(pk)
        events = []
        if Team_championship.objects.filter(object_id = client.pk).exists():
            aux = list(Team_championship.objects.filter(object_id=client.pk))
            for a in aux:
                events.append(a)
        if Single_championship.objects.filter(object_id=client.pk).exists():
            aux = list(Single_championship.objects.filter(object_id=client.pk)) 
            for a in aux:
                events.append(a)
        if Other_event.objects.filter(object_id=client.pk).exists():
            aux = list(Other_event.objects.filter(object_id=client.pk))
            for a in aux:
                events.append(a)
        return events

    @staticmethod
    def set_observation(data,**kwargs):
        if kwargs:
            event = kwargs['event']
            event.observation = data
            event.save()
        else:
            print("buscar el evento para agregarle una observacion")
    
    @staticmethod    
    def count_team(event,_type_):
        if _type_ == 'add':
            if event.ins_teams < event.max_teams:
                event.ins_teams +=1
        elif _type_ == 'subs':
            if event.ins_teams > 0:
                event.ins_teams -=1
        event.save()
    
    @staticmethod
    def count_athletes(event,_type_):
        if _type_ == 'add':
            if event.ins_athletes < event.max_athletes:
                event.ins_athletes +=1
        elif _type_ == 'subs':
            if event.ins_athletes > 0:
                event.ins_athletes -=1
        event.save()
    
    @staticmethod
    def count_person(event,_type_):
        if _type_ == 'add':
            if event.ins_person < event.max_person:
                event.ins_person +=1
        elif _type_ == 'subs':
            if event.ins_person > 0:
                event.ins_person -=1
        event.save()
#:::::::End event factory:::::::::::::

#:::::::signals event factory:::::::::::::

#:::::::End signals event factory:::::::::::::

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
        except Exception as e:
            print("algo fallo en la inscripcion del equipo",e)
    @staticmethod
    def get_teams(id_event):
        Qteams = Team.objects.filter(event=id_event)
        return Qteams
    @staticmethod
    def get_event_teams(id_event):
        Qteams = list(Team.objects.filter(event=id_event).values())
        return Qteams
    @staticmethod
    def get_team(id_team):
        Qteam = Team.objects.get(pk=id_team)
        return Qteam
    @staticmethod
    def count_ins(team,position,_type_):
        if _type_ == 'add':
            if position == 'Titular':
                if team.athletes < team.max_atheteles:
                    team.athletes +=1
            elif position == 'Reserva':
                if team.reserve < team.max_reserve:
                    team.reserve +=1
        elif _type_ == 'subs':
            if position == 'Titular':
                if team.athletes > 0:
                    team.athletes -=1
            elif position == 'Reserva':
                if team.reserve > 0:
                    team.reserve -=1
        team.save()

#:::::::signals teams factory:::::::::::::
def add_team(sender,instance,**kwargs):
    print("revisando si se llama esta funcion")
    Event_factory.count_team(instance.event,'add')

def substract_team(sender,instance,**kwargs):
    Event_factory.count_team(instance.event,'subs')

post_save.connect(add_team,sender=Team)
post_delete.connect(substract_team,sender=Team)

#:::::::End signals teams factory:::::::::::::

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
        return "Deportista: %s %s | Edad: %s | Equipo: %s" % (self.first_name,self.last_name,self.age,self.my_team)

class Other_person(iPerson):
    event = models.ForeignKey(Other_event,blank=False,null=False,on_delete=models.CASCADE,default=1)

class Athlete_factory():
    @staticmethod
    def get_inscribed(**kwargs):
        _event_, _id_ = kwargs['type'],kwargs['id']
        if _event_ == 'other':
            #print("CARGAR LAS PERSONAS INSCRITAS")
            all_data = Other_person.objects.filter(event=_id_)
        if _event_ == 'single':
            #print("CARGAR LOS DEPORTISTAS INSCRITOS")
            all_data = Athlete.objects.filter(event=_id_)
        if _event_ == 'team':
            #print("CARGAR LOS TEAMS INSCRITOS")
            all_data = Team_Factory.get_teams(id_event=_id_)
        return all_data

    @staticmethod
    def get_event_persons(event):
        all_person = Other_person.objects.all(event.pk)
        return all_person

    @staticmethod
    def get_event_athletes(event):
        all_athlete = Athlete.objects.filter(event=event.pk)
        return all_athlete
    
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
    def person_inscription(data,event):
        try:
            # first_name | last_name | age | email | status | event 
            new_person = Other_person( first_name=data['first_name'],last_name=data['last_name'],age=data['age'],
                                       email=data['email'],event=event)
            new_person.save()
        except Exception as e:
            print("Problemas al inscribir una persona a un evento: --> ",e)

    @staticmethod
    def athlete_inscription(data,event):
        try:
            print("quiero inscribir a un atlete inscription")
            # first_name | last_name | age | email | status | results | event | club     
            new_athlete = Athlete( first_name=data['first_name'],last_name=data['last_name'],age=data['age'],
                                   email=data['email'],event=event,club=data['club'])
            new_athlete.save()
            #Event_factory.new_athlete(event)
        except Exception as e:
            print("problemas al inscribir un deportista a un torneo: --> ",e)

    @staticmethod
    def athlete_team_inscription(data,team):
        try:
            # first_name | last_name | age | email | status | results | event | club     
            new_athlete_team = Athlete_team( first_name=data['first_name'],last_name=data['last_name'],age=data['age'],
                                             email=data['email'],my_team=team,position=data['position'])
            new_athlete_team.save()
            """ANALIZAR SI ES NECESARIO UNA FUNCION QUE ACTUALICE CUPO"""
        except Exception as e:
            print("problemas al inscribir un deportista a un torneo: --> ",e)
    
    @staticmethod
    def create_athlete(**kwargs):
        print("ANTIGUA FUNCION DE CREACION DE ATLETA, REVISAR DONDE SE ESTA LLAMANDO")


#:::::::signals teams factory:::::::::::::
def add_athlete(sender,instance,**kwargs):
    Event_factory.count_athletes(instance.event,'add')

def substract_athlete(sender,instance,**kwargs):
    Event_factory.count_athletes(instance.event,'subs')

def add_person(sender,instance,**kwargs):
    Event_factory.count_person(instance.event,'add')

def substract_person(sender,instance,**kwargs):
    Event_factory.count_person(instance.event,'subs')

def add_athlete_team(sender,instance,**kwargs):
    Team_Factory.count_ins(instance.my_team,instance.position,'add')

def substract_athlete_team(sender,instance,**kwargs):
    Team_Factory.count_ins(instance.my_team,instance.position,'subs')

post_save.connect(add_athlete,sender=Athlete)
post_delete.connect(substract_athlete,sender=Athlete)
post_save.connect(add_athlete_team,sender=Athlete_team)
post_delete.connect(substract_athlete_team,sender=Athlete_team)
post_save.connect(add_person,sender=Other_person)
post_delete.connect(substract_person,sender=Other_person)
#:::::::End signals teams factory:::::::::::::