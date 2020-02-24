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
from dateutil.parser import parse


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
        duplicate_map = self.count_duplicates(tuple_lines)
        tuple_lines = self.remove_duplicates(tuple_lines,duplicate_map)
        tuple_lines = self.compute_answer_index(tuple_lines)
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
                    existing_dictionary = consent_dictionnary[key]  
                    existing_dictionary.update(parsed_line) ##append new data to the session data
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
    
    def count_duplicates(self,tuples):
        '''
        The rule used is worker_id + session_id + microtask_id
        '''
        count_map = {"0:0:0":1} 
        duplicate_map = {"0:0:0":2}
        for line in tuples:
            worker_id = line["worker_id"]
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
   
    def increment_answerCount(self,countMap, session_id,worker_id):
        counter = 1
        key = session_id +"_"+ worker_id
        if(key in countMap.keys()):
            counter = countMap[key]+1
        countMap[key] = counter
        return (countMap)
   
    def compute_answer_index(self,tuples):
        answerIndex_map = {"0:0":1} 
        final_tuples =[]
        for line in tuples:
            key = line["session_id"] +"_"+  line["worker_id"]
            answerIndex_map = self.increment_answerCount(answerIndex_map, line["session_id"], line["worker_id"])
            line["answer_index"] = answerIndex_map[key]
            final_tuples.append(line)
        return(final_tuples)
   
    def parse_all_to_dictionary(self,file_lines,worker_data,parser):
        """parse all lines into dictionary tuples, return a list of these tuples"""
        parsed_lines=[]
        for line in file_lines:
            newLine = parser.parse_session_line_to_dictionary(line)  #_line_to_dictionary(line)
            if(newLine.__len__()>0):
                worker_id = newLine["worker_id"]
                if(worker_id in worker_data):
                    worker_data_dictionary = worker_data[worker_id]
                    newLine.update(worker_data_dictionary) ##append worker data to the session data
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
        self.root = 'C://Users//Christian//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-2_2015//'
        self.output ='C://Users//Christian//Documents//GitHub//DW_Microtasks//output//'
        self.testInput = 'C://Users//Christian//Documents//GitHub//DW_Microtasks//test//'
    
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
                                    self.get_header_arff(),
                                    tuple_size=32
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
                    "@ATTRIBUTE time_stamp STRING",
                    "@ATTRIBUTE event  {MICROTASK}",
                    "@ATTRIBUTE worker_id  STRING",
                    "@ATTRIBUTE file_name STRING",
                    "@ATTRIBUTE session_id STRING",
                    "@ATTRIBUTE microtask_id STRING",
                    "@ATTRIBUTE question_type {VARIABLE_DECLARATION,METHOD_INVOCATION,IF_CONDITIONAL,FOR_LOOP,WHILE_LOOP}",
                    "@ATTRIBUTE question STRING",
                    "@ATTRIBUTE answer {NO_THERE_IS_NOT_AN_ISSUE, I_DO_NOT_KNOW, YES_THERE_IS_AN_ISSUE}",
                    "@ATTRIBUTE answer_index NUMERIC",
                    "@ATTRIBUTE confidence NUMERIC",
                    "@ATTRIBUTE difficulty NUMERIC",
                    "@ATTRIBUTE duration NUMERIC",
                    "@ATTRIBUTE explanation STRING",
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
                    "@ATTRIBUTE quit_fileName STRING",
                    "@ATTRIBUTE quit_reason STRING",
                    "",
                    "@DATA",
                    ""
                    ]
        return header_lines     

#experience {Hobbyist, Professional_Developer, Graduate_Student,Undergraduate_Student, Other}"
#quit_reason {TOO_DIFFICULT, TOO_LONG, TOO_BORING, OTHER}",

class Merger_1(Merge_Files):
    '''
    Merges files from experiment 1. It uses two parsers 1 and 2
    '''

    def __init__(self):
        '''
        Initialize folders 
        '''
        self.root = 'C://Users//Christian//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-1_2014//'
        self.output ='C://Users//Christian//Documents//GitHub//DW_Microtasks//output//' 
        self.testInput ='C://Users//Christian//Documents//GitHub//DW_Microtasks//test//'
        
    def process(self):
        """process the two files"""        
        
        '''Add Year Month Day to files. Started on 24 Oct 2014'''
        self.append_year_month_day(";", self.root, "session_Run1-Total-25oct.log", 24)
        self.append_year_month_day(";", self.root, "consent_Run1-Total-25oct.log", 24)
        
        self.append_year_month_day("%", self.root, "session_Run2-28oct.log", 25)
        self.append_year_month_day("%", self.root, "consent_Run2-28oct.log", 25)


        tuple_lines_1 = self.run(
                               self.output + "t-stamp_session_Run1-Total-25oct.log",
                               self.output + "t-stamp_consent_Run1-Total-25oct.log",
                               #self.testInput + "sessionTestData.txt",
                               #self.testInput + "consentTestData.txt",
                                Parser.Parser.factory_method(self,worker_id_suffix='1', separator1=";", separator2="=")
                               ) 
        
        tuple_lines_2 = self.run(
                                 self.output + "t-stamp_session_Run2-28oct.log",
                                 self.output + "t-stamp_consent_Run2-28oct.log",
                                 Parser.Parser.factory_method(self,worker_id_suffix='2',separator1="%",separator2="%")
                               ) 
        
        tuple_lines = tuple_lines_1 + tuple_lines_2
        
        #tuple_lines = self.add_year_month_day(tuple_lines)
        
#         #Test files
#         tuple_lines = self.run("C://Users//Chris//Documents//GitHub//DW_Microtasks//test//sessionTestData_2.txt",
#                                 "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//consentTestData2.txt",
#                                 suffix='2',separator="%") #file_name="session_Run1-Total-25oct.log",suffix='1')
         
        """tuple_lines = tuple_lines + self.run("C://Users//Christian//Documents//GitHub//DW_Microtasks//test//testData_2.txt", suffix='2') #file_name="session_Run2-28oct.log", suffix='2')"""
        writer = FileReaderWriter()
        writer.write_session_log_arff(tuple_lines, 
#                                       self.output+'consolidated_TEST_Run2.arff',
                                    self.output+'consolidated_Final_Experiment_1.arff',
                                    self.get_header_arff(),
                                    tuple_size=24
                                    )

# {11ByteArrayBuffer_buggy.java,8buggy_AbstractReviewSection_buggy.txt,1buggy_ApacheCamel.txt,9buggy_Hystrix_buggy.txt,13buggy_VectorClock_buggy.txt,10HashPropertyBuilder_buggy.java,3buggy_PatchSetContentRemoteFactory_buggy.txt,7buggy_ReviewTaskMapper_buggy.txt,6ReviewScopeNode_buggy.java,2SelectTranslator_buggy.java}
    
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
                    "@ATTRIBUTE time_stamp  STRING",
                    "@ATTRIBUTE event  {MICROTASK}",
                    "@ATTRIBUTE worker_id  STRING",
                    "@ATTRIBUTE session_id STRING",
                    "@ATTRIBUTE microtask_id STRING",
                    "@ATTRIBUTE file_name STRING",
                    "@ATTRIBUTE question STRING",
                    "@ATTRIBUTE answer {NO, PROBABLY_NOT, I_CANT_TELL, PROBABLY_YES, YES}",
                    "@ATTRIBUTE answer_index NUMERIC",
                    "@ATTRIBUTE duration NUMERIC",
                    "@ATTRIBUTE explanation STRING",
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
    
    
    def append_year_month_day(self, separator1, file_path, file_name, start_day):
    
        file_lines = self.load_file(file_path+file_name)
        file_lines = self.consolidate_broken_lines(file_lines)
        line_list=[]
        i=0
        for line in file_lines:
            tokens = re.split(separator1,line)    
            tuple_line = {"time_stamp":0,"content":0}
            
            '''Capture TimeStamp'''
            time_stamp_event = tokens[0]
            time_stamp = time_stamp_event[:12] 
            tuple_line["time_stamp"] = time_stamp            
            tuple_line["content"] = line
            line_list.append(tuple_line)
        
        '''append the Year, Month, Day'''
        last_day = self.add_year_month_day(line_list, file_name, start_day)
        
        return(last_day)
        
        
    def add_year_month_day(self,tuple_lines,file_name,start_day):
        '''
        add the information about the year, month, and day of the experiment
        to the time_stamp field
        '''

        first_dt = parse(tuple_lines[0]['time_stamp'])
        current_day = start_day #experiment started on October 24, 2014
        hour = first_dt.hour 
        minute = first_dt.minute
        second = first_dt.second
        microsecond = first_dt.microsecond
        dt_previous = parse(str("2014")+" "+str("10")+" "+str(start_day)+" "+
                            str(hour)+":"+str(minute)+
                            ":"+str(second)+"."+str(microsecond))
        
        length = len(tuple_lines)
        tuple_lines[0]['time_stamp'] = "\"" +dt_previous.strftime("%Y %m %d %H:%M:%S.%f") +"\""
        tuple_lines[0]['content'] = str("2014")+" "+str("10")+" "+str(start_day) +" "+ tuple_lines[0]['content']

        #dt_current = dt_previous
        for i in range(1,length):
            dt_current = parse(tuple_lines[i]['time_stamp'])
            hour = dt_current.hour
            minute = dt_current.minute
            second = dt_current.second
            microsecond = dt_current.microsecond
            #check if crossed the day (e.g., current hour smaller than previous hour)
            if(dt_current.hour < dt_previous.hour):
                current_day +=1
                #print(dt_current.hour)
                #print(dt_previous.hour)
                #dt_previous += datetime.timedelta(days=1)
            
            dt_current = parse(str("2014")+" "+str("10")+" "+str(current_day)+" "
                       +str(hour)+":"+str(minute)+
                        ":"+str(second)+"."+str(microsecond))
        
            dt_previous = dt_current #reset previous date
            tuple_lines[i]['time_stamp'] = "\"" +dt_previous.strftime("%Y %m %d %H:%M:%S.%f") +"\""
            content = tuple_lines[i]['content']
            tuple_lines[i]['content'] = str("2014")+" "+str("10")+" "+str(current_day) +" " +content

                
        '''write to file'''
        output_file_path = self.output+"t-stamp_"+file_name
        writer = FileReaderWriter()
        writer.write_lines_to_file(tuple_lines,output_file_path)

        return (current_day)
    
#CONTROLLER CODE

merger = Merge_Files()
parser = merger.merger_factory(experiment="1")
parser.process()
#parser = merger.merger_factory(experiment="2")
#parser.process()
