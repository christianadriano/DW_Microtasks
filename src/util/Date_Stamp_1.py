'''
Created on Nov 13, 2019

Add a date stamp for experiment-1 log lines.

@author: Christian
'''
from dateutil.parser import parse

class Date_Stamp_1(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Empty constructor
        '''
    
    def add_year_month_day(self,tuple_lines):
        '''
        add the information about the year, month, and day of the experiment
        to the time_stamp field
        '''
        first_dt = parse(tuple_lines[0]['time_stamp'])
        current_day = 24 #experiment started on October 24, 2014
        hour = first_dt.hour 
        minute = first_dt.minute
        second = first_dt.second
        microsecond = first_dt.microsecond
        dt_previous = parse("2014 10 24 "+str(hour)+":"+str(minute)+
                            ":"+str(second)+"."+str(microsecond))
        
        length = len(tuple_lines)
        tuple_lines[0]['time_stamp'] = "\"" +dt_previous.strftime("%Y %m %d %H:%M:%S.%f") +"\""
                        
        for i in range(1,length):
            dt = parse(tuple_lines[i]['time_stamp'])
            hour = dt.hour
            minute = dt.minute
            second = dt.second
            microsecond = dt.microsecond
            #check if crossed the day (e.g., current hour smaller than previous hour)
            if(dt.hour<dt_previous.hour):
                current_day +=1
                #dt_previous += datetime.timedelta(days=1)
            dt = parse("2014 10 "+str(current_day)+" "+str(hour)+":"+str(minute)+
                            ":"+str(second)+"."+str(microsecond))
        
            dt_previous = dt #reset previous date
            tuple_lines[i]['time_stamp'] = "\"" +dt_previous.strftime("%Y %m %d %H:%M:%S.%f") +"\""


        return (tuple_lines)
       
