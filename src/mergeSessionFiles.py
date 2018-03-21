'''
Created on Mar 15, 2018

Processess SessionLog and ConsentLog Files
- Remove extra-lines
- Add information of user

@author: Chris
'''
#from idlelib.browser import file_open
import re

class SessionLoader:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Empty constructor
        '''
        
     
    def run(self):
        """ coordinate the loading, Cleaning, Formating, and Writing of Session Files"""
        file_header = ['time_stamp','event','workerID','microtaskID','fileName','question','answer','duration','explanation']
        file_lines = [file_header]
        #Load file into a dictionary 
        root = 'C://Users//Chris//Dropbox (Personal)//FaultLocalization_Microtasks_data//'
        path2014 = root + 'Experiment-1_2014//'
        file_name = 'session_Run1-Total-25oct.log'
        file_path = path2014 + file_name
        file_lines = self.load_file(file_path,file_lines)
        file_lines = self.consolidate_broken_explanations(file_lines)

    def load_file(self,file_path):
        """Read a file and writes the content in a list of dictionaries [{lineNuber:LineContent}]"""
        file_lines=[]
        with open(file_path) as file_object:
            for line in file_object:
                file_lines.append(line) 
                #print(file_lines)
        file_object.close()
        return file_lines
                
    def consolidate_broken_lines(self,file_lines):
        """This function cut these lines and paste the content back in the original line. Some lines were broken into multiple lines."""
        i=0
        accumulating_line=-1
        processed_lines=[]
        for line in file_lines:  
            if(not self.hasNumbers(line[0])):
                if(accumulating_line==-1):
                    accumulating_line=i-1#set line to received broken lines
                processed_lines[accumulating_line] = processed_lines[accumulating_line]+" "+line
            else:
                accumulating_line=-1 #stop accumulating extra explanation lines
                processed_lines.append(line)
                i=i+1
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