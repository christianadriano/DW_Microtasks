'''
Created on Mar 15, 2018

Processes SessionLog and ConsentLog Files
- Remove extra-lines
- Add programmer data obtain through the qualification test and demographics survey

@author: Christian Adriano
'''
#from idlelib.browser import file_open
import re
from util.FileReaderWriter import FileReaderWriter  
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
        file_session_1= self.root + "session_Run1-Total-25oct.log"
        file_session_2= self.root + "session_Run2-28oct.log"
        file_consent_1= self.root + "consent_Run1-Total-25oct.log"
        file_consent_2= self.root + "consent_Run2-28oct.log"
        
        tuple_lines = self.run(file_session_1,
                               file_consent_1,
                               suffix='1') 
        
#        Test files
#         tuple_lines = self.run("C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData.txt",
#                                "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//consentTestData.txt",
#                                suffix='1') #file_name="session_Run1-Total-25oct.log",suffix='1')
        
        """tuple_lines = tuple_lines + self.run("C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData_2.txt", suffix='2') #file_name="session_Run2-28oct.log", suffix='2')
        """
        writer = FileReaderWriter()
        writer.write_session_log_arff(tuple_lines, 
                                   self.output+'consolidated_Run1-Total-25oct.arff',
                                    self.get_header_arff())

    def run(self,session_file_name_path,consent_file_name_path, suffix):
        """ coordinate the loading, Cleaning, Formating, and Writing of Session Files"""
        """ file_name of the session log data, suffix is either 1 or 2, to indicate from which file this register came"""
        session_file_lines = ['time_stamp','event','worker_id','session_id', 'microtask_id','file_name','question','answer','duration','explanation']
        #Load file into a dictionary 
        session_file_lines = self.load_session_file_lines(session_file_name_path)
        worker_data = self.load_consent_file(consent_file_name_path,suffix)
        tuple_lines = self.parse_all_to_dictionary(session_file_lines, worker_data, suffix)
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
                 
    def load_consent_file(self,consent_file_path, suffix):
        """Load all the data from each worker on a dictionary that can be queried later on""" 
        
        """for each worker_id, keeps the data about consent, skill test, and survey"""
        consent_dictionnary = {} 
        consent_file_lines = self.load_file(consent_file_path)
        consent_file_lines = self.consolidate_broken_lines(consent_file_lines) 
        for line in consent_file_lines:
            parsed_line = self.parse_consent_line_to_dictionary(line,suffix) 
            key = parsed_line["worker_id"]
#             event = parsed_line["event"]
#             print()
#             print(parsed_line)
#             print(key)
            if(key in consent_dictionnary):
                del parsed_line["worker_id"] #remove the worker_id key-value, because we already have
                existing_dictionary = consent_dictionnary[key]  
#                 if(event=="CONSENT"):
#                     parsed_line.update(existing_dictionary)
#                     consent_dictionnary[key] = parsed_line
#                 elif(event =="SKILLTEST" or event=="SURVEY"):
                existing_dictionary.update(parsed_line)
                consent_dictionnary[key] = existing_dictionary
            else:
                consent_dictionnary[key] = parsed_line
            
        return(consent_dictionnary)
           
    def parse_consent_line_to_dictionary(self,line,suffix):
        """parse the line into a dictionary"""
        tokens = re.split(';',line)    
        time_stamp_event = tokens[0]
        time_stamp = time_stamp_event[:12]
       
        event = (re.split('\=',tokens[0])[1]).strip()
        worker_ID = re.split('\=',tokens[1])[1]+"_"+suffix
        tuple_line={"worker_id":worker_ID} #need this to find index the tuple
#         tuple_line={"event":event} #Need this later to make a decision about the order of the fields
        if(event=="CONSENT"):
            tuple_line["consent_date"] = (re.split('\=',tokens[2])[1]).strip()
        elif(event=="SKILLTEST"):
            tuple_line["test1"] = re.split('\=',tokens[2])[1]
            tuple_line["test2"] = re.split('\=',tokens[3])[1]
            tuple_line["test3"] = re.split('\=',tokens[4])[1]
            tuple_line["test4"] = re.split('\=',tokens[5])[1]
            tuple_line["grade"] =  re.split('\=',tokens[6])[1]
            tuple_line["testDuration"] = (re.split('\=',tokens[7])[1]).strip()
        elif(event=="SURVEY"):
            tcount = 3
            try:
                    ## tuple_line["session_id"] = re.split('\=',tokens[2])[1] #no need
                results = self.extract_feedback(tokens,3,"Gender=")
                tuple_line["feedback"] = results[0]
                tcount = results[1]  
                tuple_line["gender"] = re.split('\=',tokens[tcount+1])[1]
                tuple_line["years_programming"] = re.split('\=',tokens[tcount+2])[1]
                tuple_line["difficulty"] = re.split('\=',tokens[tcount+3])[1] 
                tuple_line["country"] = re.split('\=',tokens[tcount+4])[1]  
                tuple_line["age"] = re.split('\=',tokens[tcount+5])[1]  
            except:
                print("   That was no valid number.  Try again...")
                print(time_stamp)
        return (tuple_line)      
           
           
    def extract_feedback(self,tokens,index,endToken):
        """extracts the feedback text and returns next token position """
        feedback = self.replace_commas(re.split('\=',tokens[index])[1])
        index += 1
        foundEnd = False
        while (index < tokens.__len__() and not foundEnd): #means that did not find the next valid token yet
            print("feedback= " + feedback)
#             print("tokens["+str(index)+"]="+tokens[index]) 
            feedback = feedback +" " + self.replace_commas(tokens[index])
            index += 1
            if(index > tokens.__len__() or  tokens[index].find(endToken)>0 ):
                foundEnd = True
        results=[feedback,index-1]
        return (results)
        
    def match_start_tuple(self,first_eight_characters):
        """tests if the string corresponds to the beginning of new tuple NN:NN:NN"""
        isNewTuple = False
        if(re.match(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]',first_eight_characters)):
            isNewTuple = True
        else:
            isNewTuple = False
        return isNewTuple
   
    def parse_all_to_dictionary(self,file_lines,worker_data,suffix):
        """parse all lines into dictionary tuples, return a list of these tuples"""
        parsed_lines=[]
        for line in file_lines:
            newLine = self.parse_line_to_dictionary(line, suffix)
            if(newLine.__len__()>0):
                worker_id = newLine["worker_id"]
                if(worker_id in worker_data):
                    worker_data_dictionary = worker_data[worker_id]
                    newLine.update(worker_data_dictionary)
                parsed_lines.append(newLine)
        return parsed_lines
    
    def parse_line_to_dictionary(self,line,suffix):
        """parse the line into a dictionary"""
        tuple_line = []
        tokens = re.split(';',line)    
        time_stamp_event = tokens[0]
        time_stamp = time_stamp_event[:12]
        event = re.split('\=',tokens[0])[1]
        if(event=="MICROTASK"):#Ignore other events
            worker_ID = re.split('\=',tokens[1])[1]+"_"+suffix
            session_ID = re.split('\=',tokens[2])[1]
            tuple_line={"time_stamp":time_stamp,"event":event,"worker_id":worker_ID,"session_id":session_ID}  
            tuple_line["microtask_id"] = re.split('\=',tokens[3])[1]
            tuple_line["file_name"] = re.split('\=',tokens[4])[1]
            tuple_line["question"] = re.split('\=',tokens[5])[1]
            tuple_line["answer"] = re.split('\=',tokens[6])[1]
            tuple_line["duration"] =  re.split('\=',tokens[7])[1]
            tuple_line["explanation"] = self.replace_commas(self.retrieve_explanation(line))          
        return (tuple_line)
        
    def retrieve_explanation(self, line):
        """restore the explanation text, which can include semicolon and equal"""
        position = line.index("explanation=")
        return(line[position+"explanation=".__len__():line.__len__()])
    
    def replace_commas(self, explanation_text):
        """replace commas with semicolons, because the output file is in CSV format"""
        return(explanation_text.replace(",",";"))
    
    def get_header_arff(self):
        author ="Christian Medeiros Adriano"
        date="August, 2018"
        header_lines=["% 1. Title: First Failure Understanding Database",
                    "%" ,
                    "% 2. Sources:",
                    "%      (a) Creator: Christian Medeiros Adriano",
                    "%      (b) Date: August, 2018",
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
    
    """Not used"""
    def hasNumbers(self,input_string):
        """tests if the inputString contains numbers, because it should start with numbers"""
        return any(char.isdigit() for char in input_string)
         
         
myObject = SessionLoader()
myObject.__init__()
myObject.process()