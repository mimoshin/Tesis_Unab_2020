from calendar import*
from Eventos.models import Event_factory
from datetime import date

#:::CONSTANT | VARS::::
"""
*****Formato de horario disponible por dia*****
[['8:00 - 9:00 hrs','none','none','none','none','none','none'],['9:00 - 10:00 hrs','none','none','none','none','none','none'],
['10:00 - 11:00 hrs','none','none','none','none','none','none'],['11:00 - 12:00 hrs','none','none','none','none','none','none'],
['12:00 - 13:00 hrs','none','none','none','none','none','none'],['13:00 - 14:00 hrs','none','none','none','none','none','none'],
['14:00 - 15:00 hrs','none','none','none','none','none','none'],['15:00 - 16:00 hrs','none','none','none','none','none','none'],
['16:00 - 17:00 hrs','none','none','none','none','none','none'],['17:00 - 18:00 hrs','none','none','none','none','none','none'],
['18:00 - 19:00 hrs','none','none','none','none','none','none'],['19:00 - 20:00 hrs','none','none','none','none','none','none'],
['20:00 - 21:00 hrs','none','none','none','none','none','none'],['21:00 - 22:00 hrs','none','none','none','none','none','none'],
['22:00 - 23:00 hrs','none','none','none','none','none','none'],['23:00 - 24:00 hrs','none','none','none','none','none','none']]

[ [HORA,ZONA_1,ZONA_2,ZONA_3,ZONA_4,ZONA_5,ZONA_6] ]

"""
MONTHS = {'January':'Enero','February':'Febrero','March':'Marzo','April':'Abril',
          'May':'Mayo','June':'Junio','July':'Julio','August':'Agosto',
          'September':'Septiembre','October':'Octubre','November':'Noviembre','December':'Diciembre',
         }
DAYS = {'Mon':'Lunes','Tue':'Martes','Wed':'Miercoles','Thu':'Jueves','Fri':'Viernes','Sat':'Sabado','Sun':'Domingo'}


NUMBER_DAYS = ['none','none','none','none','none','none','none','none','none','none',
               'none','none','none','none','none','none','none','none','none','none',
               'none','none','none','none','none','none','none','none','none','none',
               'none']
e_dict = {'single_championship':'single','team_championship':'team','other_event':'other'}
#:::::::::::::::

#:::functions:::
def clean_disp():
    var = [['8:00 - 9:00 hrs','none','none','none','none','none','none'],['9:00 - 10:00 hrs','none','none','none','none','none','none'],
            ['10:00 - 11:00 hrs','none','none','none','none','none','none'],['11:00 - 12:00 hrs','none','none','none','none','none','none'],
            ['12:00 - 13:00 hrs','none','none','none','none','none','none'],['13:00 - 14:00 hrs','none','none','none','none','none','none'],
            ['14:00 - 15:00 hrs','none','none','none','none','none','none'],['15:00 - 16:00 hrs','none','none','none','none','none','none'],
            ['16:00 - 17:00 hrs','none','none','none','none','none','none'],['17:00 - 18:00 hrs','none','none','none','none','none','none'],
            ['18:00 - 19:00 hrs','none','none','none','none','none','none'],['19:00 - 20:00 hrs','none','none','none','none','none','none'],
            ['20:00 - 21:00 hrs','none','none','none','none','none','none'],['21:00 - 22:00 hrs','none','none','none','none','none','none'],
            ['22:00 - 23:00 hrs','none','none','none','none','none','none'],['23:00 - 24:00 hrs','none','none','none','none','none','none']]
    return var

aux = None
def calendar_month(year,month,events,data):
    h_c = custom_calendar()
    h_c.data = data
    h_c.load_events(events)
    return h_c.formatmonth(year,month)

def load_day():
    """
    Retorna la tabla de un dia 
    """
    day = clean_disp()
    text =''
    for hour in range(15):
        text = text+'<tr><td class="table-info" id=" %s-0"style="text-align:center;"> %s </td>' %(hour,day[hour][0])
        for zone in range(1,7):
            text = text+'<td class="table-warning" id="%s-%s"><button class="btn"></button></td>'% (hour,zone)
    return text

def load_events_day(events):
    aux_c = custom_calendar()
    aux_c.disponibility = clean_disp()
    for event in events:
        if event.get_type() == 'Dep':
            """
            Evento dependiente de una solicitud
            """
            e_day = event.e_request.event_date.day
            e_title,e_zone = event.e_request.event_title, event.e_request.event_place
            i_hour,f_hour  = event.e_request.init_hour, event.e_request.finish_hour
            aux_c.hour_zone(e_title,e_zone,i_hour,f_hour)
        elif event.get_type() == 'Ind':
            """
            Evento independiente de una solicitud
            """
            
            class_type = str(event.content_type).split('|')[1]
            class_type = class_type[1:]
            Qevent = Event_factory.get_event(e_dict[class_type],event.object_id)                
            e_day = event.event_date.day
            e_title,e_zone = Qevent.event_title, Qevent.event_place 
            i_hour,f_hour  = Qevent.init_hour, Qevent.finish_hour
            aux_c.hour_zone(e_title,e_zone,i_hour,f_hour)
    
    day = aux_c.disponibility
    text =''
    for hour in range(15):
        text = text+'<tr><td class="table-info" id=" %s-0"style="text-align:center;"> %s </td>' %(hour,day[hour][0])
        for zone in range(1,7):
            if day[hour][zone] == 'none':
                text = text+'<td class="table-warning" id="%s-%s"><button class="btn"></button></td>'% (hour,zone)
            else:
                text = text+'<td class="table-warning" id="%s-%s"><button class="btn">%s</button></td>' % (hour,zone,day[hour][zone])
    
    text = text+'</tr>'
    try:
        #data = aux_c.disponibility
        aux_c.__delattr__()
    except:
        pass

    return text

def define_time(month,year):    
    if month == 12: 
        p_m = month-1
        n_m = 1
        p_y = year-1
        n_y = year+1
    elif month == 1:
        p_m = 12
        n_m = month+1
        p_y = year-1
        n_y = year+1
    else:
        p_m = month-1
        n_m = month+1
        p_y = year-1
        n_y = year+1

    return p_m,n_m,p_y,n_y
    
def get_data_time(**kwargs):
    """
    carga los datos del mes y año 
    tanto previo, actual y siguiente
    """
    today = date.today()
    if kwargs:
        if kwargs.get('Month') and kwargs.get('Year'):
            month = int(kwargs['Month'])
            year = int(kwargs['Year'])
            if month > 12 :
                month = 12
                prev_month,next_month,prev_year,next_year = define_time(month,year)
            elif month <1:
                month = 1
                prev_month,next_month,prev_year,next_year = define_time(month,year)
            else:
                prev_month,next_month,prev_year,next_year = define_time(month,year)
            
                
    else:
        year = int(today.year)
        month = int(today.month)
        prev_month,next_month,prev_year,next_year = define_time(month,year)

    
    data_time = {'prev_year':prev_year,'year':year,'next_year':next_year,
                 'prev_month':prev_month,'month':month,'next_month':next_month} 
                           
    return data_time

#:::::::::::::::


class custom_calendar(HTMLCalendar):
    def load_events(self,events):
        self.events = events
        self.total_days = NUMBER_DAYS
    
    def hour_zone(self,title,zone,init,finish):
        duration = finish.hour-init.hour
        for hour in range(duration):
            aux = (init.hour+hour)-8
            self.disponibility[(init.hour+hour)-8][int(zone)] = title

    def formatday(self, day, weekday):
        self.disponibility = clean_disp()
        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            d= ''
            elist = self.events
            day_count = 0
            if elist:
                #print('lista d eeventos',elist)
                for event in elist:
                    if event.get_type() == 'Dep':
                        """
                        Evento dependiente de una solicitud
                        """
                        e_day = event.e_request.event_date.day
                        if day == e_day:
                            e_title,e_zone = event.e_request.event_title, event.e_request.event_place
                            i_hour,f_hour  = event.e_request.init_hour, event.e_request.finish_hour

                            self.hour_zone(e_title,e_zone,i_hour,f_hour)
                            self.total_days[day-1] = self.disponibility
                            if day_count<3:
                                d += f'<li type="_event_">'+e_title+'</li>'                            
                            elif day_count >=3:
                                d += f'<li class="d-none" type="_event_">'+e_title+' </li>'    
                            day_count+=1 

                    elif event.get_type() == 'Ind':
                        """
                        Evento independiente de una solicitud
                        """
                        e_day = event.event_date.day                    
                        if day == e_day:
                            class_type = str(event.content_type).split('|')[1]
                            class_type = class_type[1:]
                            Qevent = Event_factory.get_event(e_dict[class_type],event.object_id)
                        
                            e_title,e_zone = Qevent.event_title, Qevent.event_place 
                            i_hour,f_hour  = Qevent.init_hour, Qevent.finish_hour

                            self.hour_zone(e_title,e_zone,i_hour,f_hour)
                            self.total_days[day-1] = self.disponibility
                            if day_count<3:
                                d += f'<li type="_event_">'+e_title+'</li>'                            
                            elif day_count >=3:
                                d += f'<li class="d-none" type="_event_">'+e_title+' </li>'    
                            day_count+=1 
                        
            if day_count == 0:
                self.total_days[day-1] = clean_disp()
              
            if day_count>3:
                if day_count-3 == 1:
                    d+= f'<li type="more" > 1 evento mas</li>'
                else:
                    d+= f'<li type="more" >'+str(day_count-3)+' eventos mas</li>'
           
            return '<td class="day %s"id="%d"><span>%d</span><ul class="event_list"> %s </ul></td>' % (self.cssclasses[weekday], day,day,d)

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        my_day = DAYS[day_abbr[day]]
        return '<th class="%s">%s</th>' % (self.cssclasses_weekday_head[day], my_day)

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<tr>%s</tr>' % s

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        
        DATA_DIC | Este diccionario contiene los datos necesarios para definir los botones siguiente y anterior
        {'year':year,'next_year':next_year,'prev_year':prev_year,
         'month':month,'prev_month':prev_month,'next_month':next_month}
        
        if next_month == 1: month = ['next_month'] | year = ['next_year']
        else: month = ['next_month'] | year = ['year']
        
        if prev == 12: month = ['prev_month'] | year = ['prev_year']
        else: month = ['prev_month'] | year = ['year']
        
        """

        if self.data['next_month'] == 1 :
            next_button = "<th><a href='/Logistica?month=%s&year=%s' class='btn btn-sm btn-success '>Mes Siguiente</a></th>" % (self.data['next_month'],self.data['next_year'])
        else:
            next_button = "<th><a href='/Logistica?month=%s&year=%s' class='btn btn-sm btn-success '>Mes Siguiente</a></th>" % (self.data['next_month'],self.data['year'])
        
        if self.data['prev_month'] == 12:
            prev_button = "<th><a href='/Logistica?month=%s&year=%s' class='btn btn-sm btn-success '>Mes Anterior</a></th>" % (self.data['prev_month'],self.data['prev_year'])
        else:
            prev_button = "<th><a href='/Logistica?month=%s&year=%s' class='btn btn-sm btn-success '>Mes Anterior</a></th>" % (self.data['prev_month'],self.data['year'])        

        if withyear:
            month = MONTHS[month_name[themonth]]
            s = '%s %s' % (month, theyear)
        else:
            s = '%s' % month_name[themonth]
        return '<tr class="all-white"> %s <th colspan="5" class=" %s" > %s </th> %s </td>' % (prev_button, self.cssclass_month_head, s, next_button)
        

    def formatmonth(self, theyear, themonth,withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a('<thead class="head-success">')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('</thead>')
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return {'calendar':''.join(v),'disp_days':self.total_days}