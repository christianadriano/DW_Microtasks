'''
Created on August 17, 2018

Processes SessionLog and ConsentLog Files for SECOND Run Experiment 1
- Remove extra-lines
- Add programmer data obtain through the qualification test and demographics survey

@author: Christian Medeiros Adriano
'''
#from idlelib.browser import file_open
import re
from util.FileReaderWriter import FileReaderWriter  
from parserFactory import Parser
from _overlapped import NULL

class SessionLoader:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Empty constructor
        '''
        self.root = 'C://Users//Chris//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-1_2014//'
        self.output ='C://Users//Chris//Documents//GitHub//DW_Microtasks//test//' 
        
    def process(self):
        """process the two files"""
        
        tuple_lines_1 = self.run(
                                self.root + "session_Run1-Total-25oct.log",
                                self.root + "consent_Run1-Total-25oct.log",
                                Parser.Parser.factory_method(self,worker_id_suffix='1', separator1=";", separator2="=")
                               ) 
        
        tuple_lines_2 = self.run(
                                 self.root + "session_Run2-28oct.log",
                                 self.root + "consent_Run2-28oct.log",
                                 Parser.Parser.factory_method(self,worker_id_suffix='2',separator1="%",separator2="%")
                               ) 
        
        tuple_lines = tuple_lines_1 + tuple_lines_2
        
#         #Test files
#         tuple_lines = self.run("C://Users//Chris//Documents//GitHub//DW_Microtasks//test//sessionTestData_2.txt",
#                                 "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//consentTestData2.txt",
#                                 suffix='2',separator="%") #file_name="session_Run1-Total-25oct.log",suffix='1')
         
        """tuple_lines = tuple_lines + self.run("C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData_2.txt", suffix='2') #file_name="session_Run2-28oct.log", suffix='2')"""
        writer = FileReaderWriter()
        writer.write_session_log_arff(tuple_lines, 
#                                       self.output+'consolidated_TEST_Run2.arff',
                                    self.output+'consolidated_Final_Experiment_1.arff',
                                    writer.get_header_arff())

    def run(self,session_file_name_path,consent_file_name_path, parser):
        """ coordinate the loading, Cleaning, Formating, and Writing of Session Files"""
        """ file_name of the session log data, suffix is either 1 or 2, to indicate from which file this register came"""
        #Load file into a dictionary 
        session_file_lines = self.load_session_file_lines(session_file_name_path)
        worker_data = self.load_consent_file(consent_file_name_path, parser)
        tuple_lines = self.parse_all_to_dictionary(session_file_lines, worker_data, parser)
        #print file_lines to file
        return (tuple_lines)

    def load_session_file_lines(self,file_path):
        file_lines = self.load_file(file_path)
        file_lines = self.consolidate_broken_lines(file_lines)
        return file_lines

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
            if(not self.match_start_tuple(line)):
                if(accumulating_line==-1):
                    accumulating_line=i-1#set line to received broken lines
                processed_lines[accumulating_line] = processed_lines[accumulating_line]+" "+line.strip("\n")
            else:
                accumulating_line=-1 #stop accumulating extra explanation lines
                processed_lines.append(line.strip("\n"))
                i=i+1
        return processed_lines
                 
    def load_consent_file(self,consent_file_path,parser):
        """Load all the data from each worker on a dictionary that can be queried later on"""    
        """for each worker_id, keeps the data about consent, skill test, and survey"""
        consent_dictionnary = {} 
        consent_file_lines = self.load_file(consent_file_path)
        consent_file_lines = self.consolidate_broken_lines(consent_file_lines) 
        for line in consent_file_lines:
            parsed_line = parser.parse_consent_line_to_dictionary(line) 
            key = parsed_line["worker_id"]
            if(key in consent_dictionnary):
                del parsed_line["worker_id"] #remove the worker_id key-value, because we already have
                existing_dictionary = consent_dictionnary[key]  
                existing_dictionary.update(parsed_line)
                consent_dictionnary[key] = existing_dictionary
            else:
                consent_dictionnary[key] = parsed_line        
        return(consent_dictionnary)
             
    def match_start_tuple(self,first_eight_characters):
        """tests if the string corresponds to the beginning of new tuple NN:NN:NN"""
        isNewTuple = False
        if(re.match(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]',first_eight_characters)):
            isNewTuple = True
        else:
            isNewTuple = False
        return isNewTuple
   
    def parse_all_to_dictionary(self,file_lines,worker_data,parser):
        """parse all lines into dictionary tuples, return a list of these tuples"""
        parsed_lines=[]
        for line in file_lines:
            newLine = parser.parse_session_line_to_dictionary(line)  #_line_to_dictionary(line)
            if(newLine.__len__()>0):
                worker_id = newLine["worker_id"]
                if(worker_id in worker_data):
                    worker_data_dictionary = worker_data[worker_id]
                    newLine.update(worker_data_dictionary)
                parsed_lines.append(newLine)
        return parsed_lines
         
myObject = SessionLoader()
myObject.__init__()
myObject.process()

# 
#  def extract_event(self,tokens,separator1,separator2):
#         event_token = tokens.rsplit("INFO  - EVENT")
#         event_token = event_token[1].rsplit(separator1)
#         index=0
#         if(event_token[0].__len__()==0):
#             index=1
#         event = event_token[index].strip()
#         
#         if(event.find(separator2)>=0):
#             event = event[1:] #removes the separator
#         return event