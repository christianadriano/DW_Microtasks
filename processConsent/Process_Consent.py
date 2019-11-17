'''
Created on Nov 13, 2019

Process only the consent files from experiments 1 and 2.
For experiment-1 merge both files into one and write a single ARFF file
For experiment-2 only convert the csv file to an ARFF file

Provide appropriate ARFF headers for both files.

@author: Christian
'''
import re
from util.FileReaderWriter import FileReaderWriter
from util.Date_Stamp_1 import Date_Stamp_1
from parserFactory import Parser

class Process_Consent:
    '''
    classdocs
    '''
    experiment_id = 0
    
    def __init__(self):
        '''
        Initialize folders (see sub-classes)
        '''
        
    def run(self,consent_file_name_path, parser):
        """ coordinate the loading, Cleaning, Formating, and Writing of Consent File"""
        #Load file into a dictionary 
        consent_dictionary = self.load_consent_file(consent_file_name_path, parser)
        consent_tuples = list(consent_dictionary.values())
        
        #duplicate_map = self.count_duplicates(consent_dictionary)
        #consent_dictionary = self.remove_duplicates(consent_dictionary,duplicate_map)
        #consent_dictionary = self.compute_answer_index(consent_dictionary)
        #print file_lines to file
        return (consent_tuples)
    
    @staticmethod
    def process_factory(experiment_id):
        '''
        instantiates the appropriate instance of merger for the experiment number
        '''
        experiment_id = experiment_id
        if(experiment_id=="1"):
            return(Process_Consent_1())
        else:
            return(Process_Consent_2()) #TODO substitute for consent_2
                  
    def load_consent_file(self,consent_file_path,parser):
        """Load all the data from each worker on a dictionary that can be queried later on"""    
        """for each worker_id, keeps the data about consent, skill test, and survey"""
        consent_dictionary = {}
        consent_file_lines = self.load_file(consent_file_path)
        consent_file_lines = self.consolidate_broken_lines(consent_file_lines) 
        for line in consent_file_lines:
            parsed_line = parser.parse_consent_line_to_dictionary(line) 
           
            if(parsed_line.__len__()>0 and ##There are lines that should not be processed, such as ERROR because they don't have a worker ID
               all(k in parsed_line.keys() for k in ("worker_id","event"))): #ignore experiment starting line, that has session=null

                worker_id = parsed_line["worker_id"]
                event = parsed_line["event"]
                
                if(self.experiment_id ==2):
                    key = worker_id +"_"+ parsed_line["file_name"] #because there are multiple entries in E2
                else:
                    key = worker_id
                    
                if(key in consent_dictionary.keys() and event!="CONSENT"):
                    existing_dictionary = consent_dictionary[key]  
#                    existing_dictionary.update(parsed_line) ##append new data from SkillTest or Survey event
                    consent_dictionary[key] = self.merge_dictionaries(parsed_line,existing_dictionary)
                else:
                   consent_dictionary[key]=parsed_line # print("Ignored: ", parsed_line) 
                #print(parsed_line)
        return(consent_dictionary)

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

    def merge_dictionaries(self,dict_current,dict_new):
        '''
        Always take the non-empty value as the final value.
        '''
        dict_final = {}
        keylist = dict_current.keys()
        for key in keylist:
            if(dict_current[key]==""):
                dict_final[key]=dict_new[key]
            else:
                dict_final[key]=dict_current[key]
        
        dict_final["event"] = dict_new["event"]
        return(dict_final)
            

    def count_duplicates(self,tuples):
        '''
        The rule used is worker_id + session_id + microtask_id
        '''
        count_map = {"0:0:0":1} 
        duplicate_map = {"0:0:0":2}
        for line in tuples:
            worker_id = line["worker_id"]
            if(self.experiment==2):
                session_id = line["session_id"]
                microtask_id = line["microtask_id"]
            
            counter = 1
            key = microtask_id+"_"+session_id +"_"+ worker_id
            if(key in count_map.keys()):
                counter = count_map[key]+1
                count_map[key] = counter
                if(counter>1):
                    duplicate_map[key] = counter
            else:
                count_map[key] = counter

            
        #print("Duplicated items:")
        #print(duplicate_map.keys())
        #print(duplicate_map) 
        return(duplicate_map)   
    
    def remove_duplicates(self,tuples, duplicate_tuples):
        
        final_tuples = []
        duplicate_keys = duplicate_tuples.keys()
        for line in tuples:
            worker_id = line["worker_id"]
            if(self.experiment_id==2):
                session_id = line["session_id"]
                microtask_id = line["microtask_id"]
            
            key = microtask_id+"_"+session_id +"_"+ worker_id
            if(key in duplicate_keys):
                duplicate_counter = duplicate_tuples[key]
                duplicate_counter = duplicate_counter-1
                duplicate_tuples[key] = duplicate_counter
                ''' Appends only the last occurrence of the duplicates'''
                if(duplicate_counter==0): 
                    final_tuples.append(line)
                    duplicate_tuples.pop(key)
            else:
                ''' Appends any line that is not contained in the duplicate_keys'''
                final_tuples.append(line)
         
        return(final_tuples)
  
  
class Process_Consent_1(Process_Consent):

    '''
    Process consent files for both runs of the experiment 1
    '''
    file_name = "Consent_Experiment_1"
    
    """Flag to identify the experiment"""
    experiment_id = 1
    
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.root = 'C://Users//Christian//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-1_2014//'
        self.output ='C://Users//Christian//Documents//GitHub//DW_Microtasks//output//'

    def process(self):
        """process the two files"""
        
        tuple_lines_1 = self.run(
                               self.root + "consent_Run1-Total-25oct.log",
                                Parser.Parser.factory_method(self,worker_id_suffix='1', separator1=";", separator2="=")
                               ) 
        
        tuple_lines_2 = self.run(
                                 self.root + "consent_Run2-28oct.log",
                                 Parser.Parser.factory_method(self,worker_id_suffix='2',separator1="%",separator2="%")
                               ) 
        
        tuple_lines = tuple_lines_1 + tuple_lines_2
        
        tuple_lines = self.add_year_month_day(tuple_lines)
                 
        """tuple_lines = tuple_lines + self.run("C://Users//Christian//Documents//GitHub//DW_Microtasks//test//testData_2.txt", suffix='2') #file_name="session_Run2-28oct.log", suffix='2')"""
        writer = FileReaderWriter()
        writer.write_session_log_arff(tuple_lines, 
                                    self.output+'consent_consolidated_Experiment_1.arff',
                                    self.get_header_arff(),
                                    tuple_size=16
                                    )

    def get_header_arff(self):
        author ="Christian Medeiros Adriano"
        date="October, 28, 2014"
        header_lines=["% 1. Title: Consent information from Experiment 1",
                    "%" ,
                    "% 2. Sources:",
                    "%      (a) Creator: Christian Medeiros Adriano",
                    "%      (b) Date of Experiment: October 20, 2014",
                    "%      (c) Paper draft = https://arxiv.org/abs/1612.03015",
                    "%" ,
                    "@RELATION Task",
                    "",
                    "@ATTRIBUTE time_stamp  STRING",
                    "@ATTRIBUTE worker_id  STRING",
                    "@ATTRIBUTE event  {CONSENT,SKILLTEST,SURVEY}",
                    "@ATTRIBUTE consent_date STRING",
                    "@ATTRIBUTE test1 {false, true}",
                    "@ATTRIBUTE test2 {false, true}",
                    "@ATTRIBUTE test3 {false, true}",
                    "@ATTRIBUTE test4 {false, true}",
                    "@ATTRIBUTE qualification_score NUMERIC",
                    "@ATTRIBUTE testDuration NUMERIC",
                    "@ATTRIBUTE feedback STRING",
                    "@ATTRIBUTE gender {Female,Male,Prefer_not_to_tell}",
                    "@ATTRIBUTE years_programming NUMERIC",
                    "@ATTRIBUTE difficulty NUMERIC",
                    "@ATTRIBUTE country STRING",
                    "@ATTRIBUTE age NUMERIC",
                    "",
                    "@DATA",
                    ""
                    ]
        return header_lines   
    
    def add_year_month_day(self,tuple_lines):
        '''
        add the information about the year, month, and day of the experiment
        to the time_stamp field
        '''
        return(Date_Stamp_1.add_year_month_day(self, tuple_lines))
     
     
class Process_Consent_2(Process_Consent):

    '''
    Process consent files the experiment 2
    '''
    file_name = "Consent_Experiment_2"
    
    """Flag to identify the experiment"""
    experiment_id = 2
    
    def __init__(self):
        '''
        Initialize folders 
        '''
        super().__init__()
        self.root = 'C://Users//Christian//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-2_2015//'
        self.output ='C://Users//Christian//Documents//GitHub//DW_Microtasks//output//'
    
    def process(self):
        """process the two files from experiment-2"""
        tuple_lines = self.run(
                                self.root + "consent-log_consolidated_final.txt",
                                Parser.Parser.factory_method(self,worker_id_suffix='3', separator1="%", separator2="%")
                               ) 
        
        writer = FileReaderWriter()
        writer.write_session_log_arff(
                                    tuple_lines, 
                                    self.output+'consent_consolidated_Experiment_2.arff',
                                    self.get_header_arff(),
                                    tuple_size=22
                                    )

    def get_header_arff(self):
        author ="Christian Medeiros Adriano"
        date="July, 2015"
        header_lines=["% 1. Title: Consent file from Experiment TWO",
                    "%" ,
                    "% 2. Sources:",
                    "%      (a) Creator: Christian Medeiros Adriano",
                    "%      (b) Date of Experiment: July, 2015",
                    "%      (c) Paper draft = https://arxiv.org/abs/1612.03015",
                    "%" ,
                    "@RELATION Task",
                    "",
                    "@ATTRIBUTE time_stamp STRING",
                    "@ATTRIBUTE event  {CONSENT,SURVEY,SKILLTEST,FEEDBACK}",
                    "@ATTRIBUTE worker_id  STRING",
                    "@ATTRIBUTE file_name STRING",
                    "@ATTRIBUTE consent_date NUMERIC",
                    "@ATTRIBUTE language STRING",
                    "@ATTRIBUTE experience String",
                    "@ATTRIBUTE gender {Female,Male,Prefer_not_to_tell,Other}",
                    "@ATTRIBUTE learned STRING",
                    "@ATTRIBUTE years_programming NUMERIC",
                    "@ATTRIBUTE country STRING",
                    "@ATTRIBUTE age NUMERIC",
                    "@ATTRIBUTE test1 {false,true}",
                    "@ATTRIBUTE test2 {false,true}",
                    "@ATTRIBUTE test3 {false,true}",
                    "@ATTRIBUTE test4 {false,true}",
                    "@ATTRIBUTE test5 {false,true}",
                    "@ATTRIBUTE qualification_score NUMERIC",
                    "@ATTRIBUTE testDuration NUMERIC",
                    "@ATTRIBUTE feedback STRING",
                    "@ATTRIBUTE quit_reason STRING",
                    "",
                    "@DATA",
                    ""
                    ]
        return header_lines     

#experience {Hobbyist, Professional_Developer, Graduate_Student,Undergraduate_Student, Other}"
#quit_reason {TOO_DIFFICULT, TOO_LONG, TOO_BORING, OTHER}"

#-------------------------------------------------------------------   
#CONTROLLER CODE

process_consent = Process_Consent()
#processor_1 = process_consent.process_factory(experiment_id="1")
#processor_1.process()
processor_2 = process_consent.process_factory(experiment_id="2")
processor_2.process()
