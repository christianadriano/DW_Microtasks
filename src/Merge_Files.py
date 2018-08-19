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

class Merge_Files:
    '''
    Abstract class that represents two merging processes. 
    One process for experiment 1 and other to experiment 2.
    '''
    
    def __init__(self):
        '''
        Initialize folders 
        '''
               
    def run(self,session_file_name_path,consent_file_name_path, parser):
        """ coordinate the loading, Cleaning, Formating, and Writing of Session Files"""
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
            if(parsed_line.__len__()>0): #There are lines that should not be processed, such as ERROR because they don't have a worker ID
                key = parsed_line["worker_id"]
                if(key in consent_dictionnary):
                    del parsed_line["worker_id"] #remove the worker_id key-value, because we already have
                    existing_dictionary = consent_dictionnary[key]  
                    existing_dictionary.update(parsed_line)
                    consent_dictionnary[key] = existing_dictionary
                else:
                    consent_dictionnary[key] = parsed_line        
        return(consent_dictionnary)
             
    def match_start_tuple(self,line):
        '''
        Tests if the line has the timestamp string, which means that the line is the 
        first data
        '''
        isNewTuple = False
        if(re.search(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]',line)):
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
    
    def process(self):
        pass
    
    def get_header_arff(self):
        pass
    
    @staticmethod
    def merger_factory(experiment):
        '''
        instantiates the appropriate instance of merger for the experiment number
        '''
        if(experiment=="1"):
            return(Merger_1())
        else:
            return(Merger_2())
        

class Merger_2(Merge_Files):
    '''
    Initialize variables to merge experiment-2 files
    '''  
    
    def __init__(self):
        '''
        Initialize folders 
        '''
        super().__init__()
        self.root = 'C://Users//Chris//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-2_2015//'
        self.output ='C://Users//Chris//Documents//GitHub//DW_Microtasks//output//'
        self.testInput = 'C://Users//Chris//Documents//GitHub//DW_Microtasks//test//'
    
    def process(self):
        """process the two files from experiment-2"""
        tuple_lines = self.run(
                                #self.testInput + "sessionTestData_3.txt",
                                #self.testInput + "consentTestData3.txt",
                                self.root + "session-log_consolidated_final.txt",
                                self.root + "consent-log_consolidated_final.txt",
                                Parser.Parser.factory_method(self,worker_id_suffix='3', separator1="%", separator2="%")
                               ) 
        
        writer = FileReaderWriter()
        writer.write_session_log_arff(
                                    tuple_lines, 
                                    self.output+'consolidated_Final_Experiment_2.arff',
                                    self.get_header_arff()
                                    )


    def get_header_arff(self):
        author ="Christian Medeiros Adriano"
        date="July, 2015"
        header_lines=["% 1. Title: Microtasks from Experiment TWO",
                    "%" ,
                    "% 2. Sources:",
                    "%      (a) Creator: Christian Medeiros Adriano",
                    "%      (b) Date of Experiment: July, 2015",
                    "%      (c) Paper draft = https://arxiv.org/abs/1612.03015",
                    "%" ,
                    "@RELATION Task",
                    "",
                    "@ATTRIBUTE time_stamp  DATE 'WW YYYY MMM DD HH:mm:ss.SSS'",
                    "@ATTRIBUTE worker_id  NUMERIC",
                    "@ATTRIBUTE file_name STRING",
                    "@ATTRIBUTE session_id   STRING",
                    "@ATTRIBUTE microtask_id NUMERIC",
                    "@ATTRIBUTE question_type {VARIABLE_DECLARATION,METHOD_INVOCATION,IF_CONDITIONAL,FOR_LOOP,WHILE_LOOP"
                    "@ATTRIBUTE question STRING",
                    "@ATTRIBUTE answer {NO THERE IS NOT AN ISSUE, I CANNOT TELL, YES THERE IS AN ISSUE}",
                    "@ATTRIBUTE confidence {1-low,2,3,4,5-high}",
                    "@ATTRIBUTE difficulty {1-low,2,3,4,5-high}",
                    "@ATTRIBUTE duration NUMERIC",
                    "@ATTRIBUTE explanation STRING",
                    "@ATTRIBUTE consent_date NUMERIC",
                    "@ATTRIBUTE test1 NUMERIC",
                    "@ATTRIBUTE test2 NUMERIC",
                    "@ATTRIBUTE test3 NUMERIC",
                    "@ATTRIBUTE test4 NUMERIC",
                    "@ATTRIBUTE test5 NUMERIC",
                    "@ATTRIBUTE grade NUMERIC",
                    "@ATTRIBUTE testDuration NUMERIC",
                    "@ATTRIBUTE language STRING",
                    "@ATTRIBUTE experience {Hobbyist, Professional_Developer, Graduate_Student,Undergraduate_Student, Other",
                    "@ATTRIBUTE learned {High School, University, Web, Other}",
                    "@ATTRIBUTE gender {Female, Male, Other}",
                    "@ATTRIBUTE years_programming NUMERIC",
                    "@ATTRIBUTE country STRING",
                    "@ATTRIBUTE age NUMERIC",
                    "@ATTRIBUTE feedback STRING",
                    "@ATTRIBUTE quit_fileName STRING",
                    "@ATTRIBUTE quit_reason {TOO DIFFICULT,TOO LONG, TOO BORING, OTHER}",
                    "",
                    "@DATA",
                    ""
                    ]
        return header_lines     

class Merger_1(Merge_Files):
    '''
    Merges files from experiment 1. It uses two parsers 1 and 2
    '''

    def __init__(self):
        '''
        Initialize folders 
        '''
        self.root = 'C://Users//Chris//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-1_2014//'
        self.output ='C://Users//Chris//Documents//GitHub//DW_Microtasks//output//' 
        
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
                                    self.get_header_arff())


    
        def get_header_arff(self):
            author ="Christian Medeiros Adriano"
            date="October, 28, 2014"
            header_lines=["% 1. Title: Microtasks from Experiment One",
                    "%" ,
                    "% 2. Sources:",
                    "%      (a) Creator: Christian Medeiros Adriano",
                    "%      (b) Date of Experiment: October 20, 2014",
                    "%      (c) Paper draft = https://arxiv.org/abs/1612.03015",
                    "%" ,
                    "@RELATION Task",
                    "",
                    "@ATTRIBUTE time_stamp  DATE 'HH:mm:ss.SSS'",
                    "@ATTRIBUTE worker_id  NUMERIC",
                    "@ATTRIBUTE session_id   STRING",
                    "@ATTRIBUTE microtask_id NUMERIC",
                    "@ATTRIBUTE file_name STRING",
                    "@ATTRIBUTE question STRING",
                    "@ATTRIBUTE answer {NO, PROBABLY_NOT, I_CANT_TELL, PROBABLY_YES, YES}",
                    "@ATTRIBUTE duration NUMERIC",
                    "@ATTRIBUTE explanation STRING",
                    "@ATTRIBUTE consent_date NUMERIC",
                    "@ATTRIBUTE test1 NUMERIC",
                    "@ATTRIBUTE test2 NUMERIC",
                    "@ATTRIBUTE test3 NUMERIC",
                    "@ATTRIBUTE test4 NUMERIC",
                    "@ATTRIBUTE grade NUMERIC",
                    "@ATTRIBUTE testDuration NUMERIC",
                    "@ATTRIBUTE feedback STRING",
                    "@ATTRIBUTE gender STRING",
                    "@ATTRIBUTE years_programming NUMERIC",
                    "@ATTRIBUTE difficulty NUMERIC",
                    "@ATTRIBUTE country STRING",
                    "@ATTRIBUTE age NUMERIC",
                    "",
                    "@DATA",
                    ""
                    ]
            return header_lines    
    
#CONTROLLER CODE

merger = Merge_Files()
parser = merger.merger_factory(experiment="1")
parser.process()



#     def run(self,session_file_name_path,consent_file_name_path, parser):
#         """ coordinate the loading, Cleaning, Formating, and Writing of Session Files"""
#         """ file_name of the session log data, suffix is either 1 or 2, to indicate from which file this register came"""
#         #Load file into a dictionary 
#         session_file_lines = self.load_session_file_lines(session_file_name_path)
#         worker_data = self.load_consent_file(consent_file_name_path, parser)
#         tuple_lines = self.parse_all_to_dictionary(session_file_lines, worker_data, parser)
#         #print file_lines to file
#         return (tuple_lines)
# 
#     def load_session_file_lines(self,file_path):
#         file_lines = self.load_file(file_path)
#         file_lines = self.consolidate_broken_lines(file_lines)
#         return file_lines
# 
#     def load_file(self,file_path):
#         """Read a file and writes the content in a list of dictionaries [{lineNuber:LineContent}]"""
#         file_lines=[]
#         with open(file_path) as file_object:
#             for line in file_object:
#                 file_lines.append(line) 
#                 #print(file_lines)
#         file_object.close()
#         return file_lines
#                 
#     def consolidate_broken_lines(self,file_lines):
#         """This function cut these lines and paste the content back in the original line. Some lines were broken into multiple lines."""
#         i=0
#         accumulating_line=-1
#         processed_lines=[]
#         for line in file_lines: 
#             if(not self.match_start_tuple(line)):
#                 if(accumulating_line==-1):
#                     accumulating_line=i-1#set line to received broken lines
#                 processed_lines[accumulating_line] = processed_lines[accumulating_line]+" "+line.strip("\n")
#             else:
#                 accumulating_line=-1 #stop accumulating extra explanation lines
#                 processed_lines.append(line.strip("\n"))
#                 i=i+1
#         return processed_lines
#                  
#     def load_consent_file(self,consent_file_path,parser):
#         """Load all the data from each worker on a dictionary that can be queried later on"""    
#         """for each worker_id, keeps the data about consent, skill test, and survey"""
#         consent_dictionnary = {} 
#         consent_file_lines = self.load_file(consent_file_path)
#         consent_file_lines = self.consolidate_broken_lines(consent_file_lines) 
#         for line in consent_file_lines:
#             parsed_line = parser.parse_consent_line_to_dictionary(line) 
#             key = parsed_line["worker_id"]
#             if(key in consent_dictionnary):
#                 del parsed_line["worker_id"] #remove the worker_id key-value, because we already have
#                 existing_dictionary = consent_dictionnary[key]  
#                 existing_dictionary.update(parsed_line)
#                 consent_dictionnary[key] = existing_dictionary
#             else:
#                 consent_dictionnary[key] = parsed_line        
#         return(consent_dictionnary)
#              
#     def match_start_tuple(self,first_eight_characters):
#         """tests if the string corresponds to the beginning of new tuple NN:NN:NN"""
#         isNewTuple = False
#         if(re.match(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]',first_eight_characters)):
#             isNewTuple = True
#         else:
#             isNewTuple = False
#         return isNewTuple
#    
#     def parse_all_to_dictionary(self,file_lines,worker_data,parser):
#         """parse all lines into dictionary tuples, return a list of these tuples"""
#         parsed_lines=[]
#         for line in file_lines:
#             newLine = parser.parse_session_line_to_dictionary(line)  #_line_to_dictionary(line)
#             if(newLine.__len__()>0):
#                 worker_id = newLine["worker_id"]
#                 if(worker_id in worker_data):
#                     worker_data_dictionary = worker_data[worker_id]
#                     newLine.update(worker_data_dictionary)
#                 parsed_lines.append(newLine)
#         return parsed_lines