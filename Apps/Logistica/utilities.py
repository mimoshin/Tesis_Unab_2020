from calendar import*


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


def calendar_month(year,month,events):
    h_c = custom_calendar()
    h_c.load_events(events)
    return h_c.formatmonth(year,month)

def load_day():
    day = ''
    for x in clean_disp():
        day+=str(x)+';'
    return day

def load_events_day(events):
    day = ''
    aux_c = custom_calendar()
    aux_c.disponibility = clean_disp()
    for x in events:
        e_day = x.e_request.event_date.day
        e_title,e_zone = x.e_request.event_title, x.e_request.event_place
        i_hour,f_hour  = x.e_request.init_hour, x.e_request.finish_hour
        aux_c.hour_zone(e_title,e_zone,i_hour,f_hour)

    for hour in aux_c.disponibility:
        day+=str(hour)+';'
    return day
    

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
                        e_title,e_zone = event.event_title, event.event_place
                        i_hour,f_hour  = event.init_hour, event.finish_hour

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
        """
        if withyear:
            month = MONTHS[month_name[themonth]]
            s = '%s %s' % (month, theyear)
        else:
            s = '%s' % month_name[themonth]
        return '<tr> <th colspan="7" class=" %s "> %s </th> </tr>' % (self.cssclass_month_head, s)
        

    def formatmonth(self, theyear, themonth,withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return {'calendar':''.join(v),'disp_days':self.total_days}