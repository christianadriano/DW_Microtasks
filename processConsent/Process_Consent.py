'''
Created on Nov 13, 2019

Process only the consent files from experiments 1 and 2.
For experiment-1 merge both files into one and write a single ARFF file
For experiment-2 only convert the csv file to an ARFF file

Provide appropriate ARFF headers for both files.

@author: Christian
'''
from Merge_Files import Merger_1

import re
from util.FileReaderWriter import FileReaderWriter
from util.Date_Stamp_1 import Date_Stamp_1
from parserFactory import Parser
from dateutil.parser import parse

class Process_Consent:
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Initialize folders (see sub-classes)
        '''
        
    def run(self,consent_file_name_path, parser):
        """ coordinate the loading, Cleaning, Formating, and Writing of Consent File"""
        #Load file into a dictionary 
        consent_dictionary = self.load_consent_file(consent_file_name_path, parser)
        duplicate_map = self.count_duplicates(consent_dictionary)
        consent_dictionary = self.remove_duplicates(consent_dictionary,duplicate_map)
        consent_dictionary = self.compute_answer_index(consent_dictionary)
        #print file_lines to file
        return (consent_dictionary)
    
    @staticmethod
    def merger_factory(experiment):
        '''
        instantiates the appropriate instance of merger for the experiment number
        '''
        if(experiment=="1"):
            return(Process_Consent_1())
        else:
            return(Process_Consent_1()) #TODO substitute for consent_2
                  
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
                    existing_dictionary = consent_dictionnary[key]  
                    existing_dictionary.update(parsed_line)
                    consent_dictionnary[key] = existing_dictionary
                    #del parsed_line["worker_id"] #remove the worker_id key-value, because we already have
                else:
                    consent_dictionnary[key] = parsed_line        
        return(consent_dictionnary)

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

    def remove_duplicates(self,tuples, duplicate_tuples):
        
        final_tuples = []
        duplicate_keys = duplicate_tuples.keys()
        for line in tuples:
            worker_id = line["worker_id"]
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
    
    def remove_duplicates(self,tuples, duplicate_tuples):
        
        final_tuples = []
        duplicate_keys = duplicate_tuples.keys()
        for line in tuples:
            worker_id = line["worker_id"]
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
    
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.root = 'C://Users//Christian//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-1_2014//'
        self.output ='C://Users//Christian//Documents//GitHub//DW_Microtasks//output//'
        self.testInput = 'C://Users//Christian//Documents//GitHub//DW_Microtasks//test//'




    def process(self):
        """process the two files"""
        
        tuple_lines_1 = self.run(
                               self.root + "consent_Run1-Total-25oct.log",
                               #self.testInput + "consentTestData.txt",
                                Parser.Parser.factory_method(self,worker_id_suffix='1', separator1=";", separator2="=")
                               ) 
        
        tuple_lines_2 = self.run(
                                 self.root + "consent_Run2-28oct.log",
                                 Parser.Parser.factory_method(self,worker_id_suffix='2',separator1="%",separator2="%")
                               ) 
        
        tuple_lines = tuple_lines_1 + tuple_lines_2
        
        tuple_lines = self.add_year_month_day(tuple_lines)
        
#         #Test files
#         tuple_lines = self.run("C://Users//Chris//Documents//GitHub//DW_Microtasks//test//sessionTestData_2.txt",
#                                 "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//consentTestData2.txt",
#                                 suffix='2',separator="%") #file_name="session_Run1-Total-25oct.log",suffix='1')
         
        """tuple_lines = tuple_lines + self.run("C://Users//Christian//Documents//GitHub//DW_Microtasks//test//testData_2.txt", suffix='2') #file_name="session_Run2-28oct.log", suffix='2')"""
        writer = FileReaderWriter()
        writer.write_session_log_arff(tuple_lines, 
#                                       self.output+'consolidated_TEST_Run2.arff',
                                    self.output+'consent_consolidated_Experiment_1.arff',
                                    self.get_header_arff(),
                                    tuple_size=24
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
                    "@ATTRIBUTE event  {CONSENT}",
                    "@ATTRIBUTE worker_id  STRING",
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
     
#-------------------------------------------------------------------   
#CONTROLLER CODE

process_consent = Process_Consent()
processor_1 = process_consent.process_factory(experiment="1")
processor_1.process()
processor_2 = process_consent.process_factory(experiment="2")
processor_2.process()