'''
Created on Mar 15, 2018

@author: Chris
'''
from idlelib.browser import file_open
from fileinput import filelineno
from Lib import tokenize

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
        
        if(hasNumber(file_line[0]):
            tokens = re.sprint(';',file_line)
            time_stamp_event = tokens[0]
            time_stamp = time_stamp_event[:12]
            event = re.split('\s-\s\=',time_stamp_event)
            event = event[2]
            workerID = tokens[2]
            microtaskID = tokens[3]
            question = tokens[4]
            answer = tokens[5]
            duration = tokens[6]
            explanation = tokens[7]
            dictionaryLine = {}
        else:
                
        
        
    def hasNumbers(inputString):
...     return any(char.isdigit() for char in inputString)

myObject = MyClass()
myObject.__init__()