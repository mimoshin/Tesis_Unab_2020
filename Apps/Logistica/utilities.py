from calendar import*

months = {'January':'Enero','February':'Febrero','March':'Marzo','April':'Abril',
          'May':'Mayo','June':'Junio','July':'Julio','August':'Agosto',
          'September':'Septiembre','October':'Octubre','November':'Noviembre','December':'Diciembre',
         }
days = {'Mon':'Lunes','Tue':'Martes','Wed':'Miercoles','Thu':'Jueves','Fri':'Viernes','Sat':'Sabado','Sun':'Domingo'}

class custom_calendar(HTMLCalendar):
    def load_events(self,events):
        self.events = events
    def formatday(self, day, weekday):
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
            for x in elist:
                day_event= x.date.split(' ')
                if day == int(day_event[0]):
                    if day_count<3:
                        d += f'<li type="_event_">'+x.event+' </li>'    
                    elif day_count >=3:
                        d += f'<li class="d-none" type="_event_">'+x.event+' </li>'    
                    day_count+=1
            
            if day_count>3:
                if day_count-3 == 1:
                    d+= f'<li type="more" > 1 evento mas</li>'
                else:
                    d+= f'<li type="more" >'+str(day_count-3)+' eventos mas</li>'
            """
            print("Dia: {0} - Eventos: {1}".format(day,day_count))
            total_list = [['ev a1'],
                          ['ev b1','ev b2'],
                          ['ev c1','ev c2','ev c3'],
                          ['ev d1','ev d2','ev d3','ev d4'],
                          ['ev e1','ev e2','ev e3','ev e4','ev e5'],
                          ['ev f1','ev f2','ev f3','ev f4','ev f5','fv 6'],
                          ['ev g1','ev g2','ev g3','ev g4','ev g5','gv 6','gv 7']] #largo 7 (0 a 6)

            index_event = len(total_list)
            for e_day in range(index_event):
                if day == e_day+1:
                    in_list = total_list[e_day]
                    large = len(in_list)
                    for event in range(large):
                        if event <3:
                            d += f'<li type="_event_">'+in_list[event]+' </li>'    
                        elif event >=3:
                            d += f'<li class="d-none" type="_event_">'+in_list[event]+' </li>'    
                            if event == large-1 and large>3:
                                if large-3 ==1:
                                    d+= f'<li type="more" >'+str(large-3)+' evento mas</li>'
                                else:
                                    d+= f'<li type="more" >'+str(large-3)+' eventos mas</li>'
            """
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
        my_day = days[day_abbr[day]]
        return '<th class="%s">%s</th>' % (
            self.cssclasses_weekday_head[day], my_day)

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
            month = months[month_name[themonth]]
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
        return ''.join(v)

def calendar_month(year,month,events):
    h_c = custom_calendar()
    h_c.load_events(events)
    data = h_c.formatmonth(year,month)
    return data

