'''
Created on Mar 15, 2018

Processess SessionLog and ConsentLog Files
- Remove extra-lines
- Add information of user

@author: Chris
'''
from idlelib.browser import file_open
import re

class SessionLoader:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        file_header = ['time_stamp','event','workerID','microtaskID','fileName','question','answer','duration','explanation']
        file_lines = [file_header]
        #Load file into a dictionary 
        root = 'C://Users//Chris//Dropbox (Personal)//FaultLocalization_Microtasks_data//'
        path2014 = root + 'Experiment-1_2014//'
        file_name = 'session_Run1-Total-25oct.log'
        file_path = path2014 + file_name
        file_lines = self.load_file(file_path,file_lines)
        file_lines = self.consolidate_broken_explanations(file_lines)
        

    def load_file(self,file_path,file_lines=[]):
        """read a file and writes the content in a list of dictionaries [{lineNuber:LineContent}]"""
        with open(file_path) as file_object:
            for line in file_object:
                file_lines.append(line) 
        #print(file_lines[0:4])
        file_object.close()
        return file_lines

 
                
    def consolidate_broken_explanations(self,file_lines):
        """This function cut these lines and paste the content back in the explanations field. Some explanation text was broken into multiple lines."""
        i=-1
        previous_index=-1
        processed_lines=1
        for line in file_lines: 
            i=i+1
            doesItHaveNumbers =  self.hasNumbers(file_lines[0])
            if(not doesItHaveNumbers):
                if (previous_index!=-1):
                    previous_index=i
                    processed_lines[previous_index] = processed_lines[previous_index]+line
                else:
                    previous_index=-1 #stop accumulating extra explanation lines
                    processed_lines = line
        return processed_lines
                    
                    
    def hasNumbers(self,input_string):
        """tests if the inputString contains numbers"""
        return any(char.isdigit() for char in input_string)
   
    def __parseLinesToDictionary__(self,file_lines):
        """parse each line into a dictionary"""
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
         
myObject = SessionLoader()
myObject.__init__()