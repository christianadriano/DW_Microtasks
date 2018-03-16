'''
Created on Mar 15, 2018

@author: Chris
'''
from idlelib.browser import file_open
import re

class MyClass(object):
    '''
    classdocs
    '''


    def __main__(self):
        '''
        Constructor
        '''
        file_header = ['time_stamp','event','workerID','microtaskID','fileName','question','answer','duration','explanation']
        file_lines = [{0:file_header}]
        #Load file into a dictionary 
        root = 'C://Users//Chris//Dropbox (Personal)//FaultLocalization_Microtasks_data//'
        path2014 = root + 'Experiment-1_2014//'
        file_name = 'session_Run1-Total-25oct.log'
        file_path = path2014 + fileName
        file_lines = self.loadFile(file_lines,file_path)
        file_lines = __consolidateBrokenExplanations__(file_lines)
        

    def loadFile(self,file_lines, file_path):
        with open(file_path) as file_object:
            i=0
            for line in file_object:
                i=i+1
                new_line = {i:line}
                file_lines.append(new_line) 
        #print(file_lines[0:4])
        file_object.close()
        return file_lines
    
  
    def hasNumbers(self,inputString):
       return any(char.isdigit() for char in inputString)


    def __parseLinesToDictionary__(self,file_lines):
            tokens = re.split(';',file_lines)
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
                
    def __consolidateBrokenExplanations__(self,file_lines):
        accumulatedLine=''#initialize and empty line
        i=-1
        previousIndex=-1
        for line in file_lines: 
             i=i+1
            if(not hasNumber(file_line[0]):
               if previousIndex!=-1:
                   previousIndex=i
               processed_lines[previousIndex] = processed_lines[previousIndex]+line
            else:
                 previosIndex=-1 #stop accumulating extra explanation lines
                 processed_lines = line
            return processed_lines
                    
   
         
myObject = MyClass()
myObject.__init__()