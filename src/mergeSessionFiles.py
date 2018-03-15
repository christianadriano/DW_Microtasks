'''
Created on Mar 15, 2018

@author: Chris
'''
from idlelib.browser import file_open
from fileinput import filelineno

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        file_header = ['time_stamp','event','workerID','microtaskID','fileName','question','answer','duration','explanation']
        line = {0:file_header}
        file_lines = [line]
        #Load file into a dictionary 
        with open('C://Users//Chris//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-1_2014//session_Run1-Total-25oct.log') as file_object:
            i=0
            for line in file_object:
                i=i+1
                new_line = {i:line}
                file_lines.append(new_line) 
        print(file_lines[0:4])
        file_object.close()

    
   # def __cleanUp_BreakExplanations__(file_lines):
   #      for i in file_lines:
        
    
    def __parseLine__(file_line):
        
        if(hasNumber(file_line[0])
        
        time_stamp = parseTimeStamp(file_line)
        event = parseEvent(file_line)
        workerID = parseWorkerID(file_line)
        microtaskID = parseMicrotaskID(file_line)
        question = parseQuestion(file_line)
        answer = parseQuestion(file_line)
        duration = parseDuration(file_line)
        explanation = parseExplanation(file_line)
        
        
        
    def hasNumbers(inputString):
...     return any(char.isdigit() for char in inputString)

myObject = MyClass()
myObject.__init__()