'''
Created on Mar 15, 2018

Processes SessionLog and ConsentLog Files
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
        self.root = 'C://Users//Chris//Dropbox (Personal)//FaultLocalization_Microtasks_data//'
        
    def process(self):
        """process the two files"""
        file_lines = self.run(filen_name="session_Run1-Total-25oct.log",suffix='1')
        file_lines.append(self.run(file_name="session_Run2-28oct.log", suffix='2'))
        return(file_lines)

    def run(self,file_name,suffix):
        """ coordinate the loading, Cleaning, Formating, and Writing of Session Files"""
        """ file_name of the session log data, suffix is either 1 or 2, to indicate from which file this register came"""
        file_header = ['time_stamp','event','workerID','microtaskID','fileName','question','answer','duration','explanation']
        file_lines = [file_header]
        #Load file into a dictionary 
        root = 'C://Users//Chris//Dropbox (Personal)//FaultLocalization_Microtasks_data//'
        path2014 = self.root + 'Experiment-1_2014//'
        file_path = path2014 + file_name  # @UndefinedVariable
        file_lines = self.load_file(file_path,file_lines)
        file_lines = self.consolidate_broken_explanations(file_lines)
        tuple_lines = self.parse_to_dictionary(file_lines, suffix)
        #print file_lines to file
        self.write_session_log_arff(tuple_lines, output_file='FailuireUnderstanding_Crowd_1.arff')

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
   
    def parse_all_to_dictionary(self,file_lines,suffix):
        """parse all lines into dictionary tuples, return a list of these tuples"""
        parsed_lines=[]
        for line in file_lines:
            parsed_lines.append(self.parse_line_to_dictionary(line, suffix))
        return parsed_lines
    
    def parse_line_to_dictionary(self,line,suffix):
        """parse the line into a dictionary"""
        tokens = re.split(';',line)    
        time_stamp_event = tokens[0]
        time_stamp = time_stamp_event[:12]
        event = re.split('\=',tokens[0])[1]
        worker_ID = re.split('\=',tokens[1])[1]+"_"+suffix
        session_ID = re.split('\=',tokens[2])[1]
        tuple_line={"time_stamp":time_stamp,"event":event,"worker_id":worker_ID,"session_id":session_ID}
        if(event=="MICROTASK"):
            tuple_line["microtask_id"] = re.split('\=',tokens[3])[1]
            tuple_line["file_name"] = re.split('\=',tokens[4])[1]
            tuple_line["question"] = re.split('\=',tokens[5])[1]
            tuple_line["answer"] = re.split('\=',tokens[6])[1]
            tuple_line["duration"] =  re.split('\=',tokens[7])[1]
            tuple_line["explanation"] = re.split('\=',tokens[8])[1]          
        return (tuple_line)
        
    def write_session_log_arff(self,tuple_lines,output_file):
        """write the content to an arff file"""
        header_lines = self.get_header_arff()
        with open(self.root+output_file, 'a') as the_file:
            for line in header_lines:     
                the_file.write(line)
                the_file.write("\n")
            for line in tuple_lines:
                the_file.write(self.convert_to_comma_separated(line.values()))
                the_file.write("\n")
    
    def convert_to_comma_separated(self,tuple_dictionary):
        list_values = list(tuple_dictionary.values())
        str_accum=''
        for item in list_values:
            str_accum = str_accum + "," + item
        str_accum = str_accum[1:str_accum.__len__()]
        return str_accum
    
    def get_header_arff(self):
        author ="Christian Medeiros Adriano"
        date="March, 2018"
        header_lines=["% 1. Title: First Failure Understanding Database",
                    "%" ,
                    "% 2. Sources:",
                    "%      (a) Creator: Christian Medeiros Adriano",
                    "%      (b) Date: March, 2018",
                    "%" ,
                    "@RELATION Task",
                    "",
                    "@ATTRIBUTE time_stamp  DATE 'HH:mm:ss.SSS'",
                    "@ATTRIBUTE event   {OPEN SESSION,MICROTASK,CLOSE SESSION}",
                    "@ATTRIBUTE worker_id  NUMERIC",
                    "@ATTRIBUTE session_id   STRING",
                    "@ATTRIBUTE microtask_id NUMERIC",
                    "@ATTRIBUTE file_name STRING",
                    "@ATTRIBUTE question STRING",
                    "@ATTRIBUTE answer {NO, PROBABLY_NOT, I_CANT_TELL, PROBABLY_YES, YES}",
                    "@ATTRIBUTE duration NUMERIC",
                    "@ATTRIBUTE explanation STRING",
                    "",
                    
                    ]
        return header_lines
         
myObject = SessionLoader()
myObject.__init__()