'''
Created on Aug 17, 2018

This module keeps the parsers that format and consolidate three files from two experiments

@author: Christian Adriano
'''
import re

class Parser:
    '''
    Super class for two types of parsers - for Run 1 and Run 2 of Experiment 1
    '''
    
    def __init__(self, worker_id_suffix, separator1, separator2):
        '''
        Constructor
        '''
        self.suffix = worker_id_suffix
        self.separator1 = separator1
        self.separator2 = separator2
        self.quote = "\""
               
    def parse_consent_line_to_dictionary(self,line):
        pass
    
    def parse_session_line_to_dictionary(self,line):
        pass
    
    @staticmethod
    def convert_to_numeric(self,boolean_word):
        '''
        Converts true to 1 and false to 0
        '''
        if(boolean_word =="true"): return(1)
        else: return(0)
        
        
    @staticmethod
    def factory_method(self,worker_id_suffix,separator1,separator2):
        if(worker_id_suffix =="1"):
            return Parser_Run1("1",separator1,separator2)
        elif (worker_id_suffix =="2"):
            return Parser_Run2("2",separator1,separator2)
        else:
            return Parser_Run3("3",separator1,separator2)
        
    def increment_answerCount(self,countMap, session_id,worker_id):
        counter = 1
        key = session_id +"_"+ worker_id
        if(key in countMap.keys()):
            counter = countMap[key]+1
        countMap[key] = counter
        return (countMap)
 
class Parser_Run3(Parser):
    '''
    Parses data from the second experiment
    '''
    suffix = "3"
    file_name = "Experiment_2"
    
    def __init__(self,suffix,separator1,separator2):
        '''
        Constructor
        '''
        super().__init__(suffix,separator1,separator2)
        self.answerIndex_map = {"0:0":1} 

     
    def parse_consent_line_to_dictionary(self,line):
        '''
        Parses the line into a dictionary
        '''
        tokens = re.split(self.separator1,line)

        event = tokens[1].strip()
        if(event=="ERROR"):
            return {}
        
        tuple_line = self.initialize_empty_fields() #guarantees that fields are aligned, regardless of missing ones.
        time_stamp_event = tokens[0]
        time_stamp = time_stamp_event[:28] 
        tuple_line["time_stamp"] = time_stamp
        tuple_line["event"] = event #note that this will be overwritten when merging with MICROTASK event      
        tuple_line["worker_id"] = tokens[3]+"_"+self.suffix #need this to find index the tuple
        tuple_line["file_name"] = tokens[5].strip() #need this to know which test version was executed 
        
        if(event=="CONSENT"):
            tuple_line["consent_date"] = tokens[7].strip()       
        elif(event=="SURVEY"):
            tuple_line["language"] = self.quote + tokens[7].replace(",",";") + self.quote
            tuple_line["experience"] = self.quote + tokens[9] + self.quote
            tuple_line["gender"] = tokens[11].replace(" ", "_")
            tuple_line["learned"] = self.quote + tokens[13].replace(",",";").replace(" ", "_").replace("\""," ") + self.quote
            tuple_line["years_programming"] = tokens[15]
            tuple_line["country"] = self.quote + tokens[17] + self.quote 
            tuple_line["age"] = tokens[19]
        elif(event=="SKILLTEST"):
            tuple_line["test1"] = Parser.convert_to_numeric(self,tokens[7].strip())
            tuple_line["test2"] = Parser.convert_to_numeric(self,tokens[9].strip())
            tuple_line["test3"] = Parser.convert_to_numeric(self,tokens[11].strip())
            tuple_line["test4"] = Parser.convert_to_numeric(self,tokens[13].strip())
            tuple_line["test5"] = Parser.convert_to_numeric(self,tokens[15].strip())
            tuple_line["qualification_score"] = tokens[17].strip()
            tuple_line["test_duration"] = tokens[19].strip()
        elif(event=="FEEDBACK"):
            tuple_line["feedback"] = self.quote + tokens[7].replace(",",";").replace("\"","\'")  + self.quote
        elif(event=="QUIT"):
            tuple_line["quit_reason"] = self.quote + tokens[7].replace(",",";").replace("THE TASK IS ","").replace(" ","_") + self.quote
        return (tuple_line)       
     
     
    def initialize_empty_fields(self):
        '''
        Initialize consent log empty fields to guarantee that columns are aligned,
         even when there is missing data
        '''
        tuple_line={}
        tuple_line["time_stamp"] = ""
        tuple_line["event"] = ""     
        tuple_line["worker_id"] = ""
        tuple_line["file_name"] = ""
        tuple_line["consent_date"] =""
        tuple_line["language"] = ""
        tuple_line["experience"] = ""
        tuple_line["gender"] = ""
        tuple_line["learned"] = ""  
        tuple_line["years_programming"] = ""
        tuple_line["country"] = ""
        tuple_line["age"] = ""
        tuple_line["test1"] =""
        tuple_line["test2"] = ""
        tuple_line["test3"] = ""
        tuple_line["test4"] = ""
        tuple_line["test5"] = ""
        tuple_line["qualification_score"] = ""
        tuple_line["test_duration"] = ""
        tuple_line["feedback"] = ""
        tuple_line["quit_reason"] = ""
        return(tuple_line)
    
    def parse_session_line_to_dictionary(self,line):
        """parse the line into a dictionary"""
        tuple_line = {}
        tokens = re.split(self.separator1,line)    
        time_stamp_event = tokens[0]
        time_stamp = self.quote + time_stamp_event[:28] + self.quote
        event = tokens[1]
        if(event=="MICROTASK"):#Ignore other events
            tuple_line = {"time_stamp":time_stamp}
            tuple_line["event"] = event
            tuple_line["worker_id"] = tokens[3]+"_"+self.suffix
            tuple_line["file_name"] = tokens[5].strip()
            tuple_line["session_id"] = tokens[7]
            tuple_line["microtask_id"] = tokens[9]
            tuple_line["question_type"] = tokens[11]
            tuple_line["question"] = self.quote + tokens[13].replace(",",";").replace("\"","\'") + self.quote
            tuple_line["answer"] = tokens[15].replace(",","").replace(" ","_").replace("N\'T","_NOT")
            #self.answerIndex_map = super().increment_answerCount(self.answerIndex_map, tuple_line["session_id"], tuple_line["worker_id"])
            tuple_line["answer_index"] = 0#self.answerIndex_map[tuple_line["session_id"] +"_"+ tuple_line["worker_id"]]
            tuple_line["confidence"] = tokens[17]
            tuple_line["difficulty"] = tokens[19]
            tuple_line["duration"] = tokens[21]
            index = line.find("explanation%") + "explanation%".__len__()
            tuple_line["explanation"] = self.quote + line[index:].replace(",",";").replace("\""," ").replace("\'"," ") + self.quote          
        return (tuple_line) 
 
class Parser_Run2(Parser):
    '''
    Parser for the run 2 of experiment 1
    '''
    suffix = "2"
    file_name = "Experiment_1"
    
    def __init__(self,suffix,separator1,separator2):
        '''
        Constructor
        '''
        super().__init__(suffix,separator1,separator2)
        self.answerIndex_map = {"0:0":1} 

     
    def parse_consent_line_to_dictionary(self,line):
        """parse the line into a dictionary"""
        tokens = re.split(self.separator1,line)    
        tuple_line = self.initialize_empty_fields()
        worker_id = tokens[3].strip()+"_"+self.suffix
        event = tokens[1].strip()
        '''Capture TimeStamp'''
        time_stamp_event = tokens[0]
        time_stamp = time_stamp_event[:23] 
        tuple_line["time_stamp"] = time_stamp
        tuple_line["event"] = event #note that this will be overwritten when merging with MICROTASK event      
        tuple_line["worker_id"]= worker_id #need this to find index the tuple    

        if(event=="CONSENT"):
            tuple_line["consent_date"] = tokens[5].strip()
        elif(event=="SKILLTEST"):
            tuple_line["test1"] = Parser.convert_to_numeric(self,tokens[5].strip())
            tuple_line["test2"] = Parser.convert_to_numeric(self,tokens[7].strip())
            tuple_line["test3"] = Parser.convert_to_numeric(self,tokens[9].strip())
            tuple_line["test4"] = Parser.convert_to_numeric(self,tokens[11].strip())
            tuple_line["qualification_score"] = tokens[13].strip()
            tuple_line["test_duration"] = tokens[15].strip()
        elif(event=="SURVEY"):
            #Do not need the event here, otherwise it will overwrite the Microtask event.
            tuple_line["feedback"] = self.quote + tokens[7].replace(",",";").replace("\"","\'")  + self.quote
            tuple_line["gender"] = tokens[9].replace(" ", "_")
            tuple_line["years_programming"] = tokens[11]
            tuple_line["difficulty"] = tokens[13]
            tuple_line["country"] = self.quote + tokens[15] + self.quote
            tuple_line["age"] = tokens[17]  
        return (tuple_line)       
     
    
    def parse_session_line_to_dictionary(self,line):
        """parse the line into a dictionary"""
        tuple_line = {}
        tokens = re.split(self.separator1,line)    
        time_stamp_event = tokens[0]
        time_stamp = time_stamp_event[:23]
        event = tokens[1]
        if(event=="MICROTASK"):#Ignore other events
            worker_id = tokens[3]+"_"+self.suffix
            session_id = tokens[5]
            tuple_line={"time_stamp":time_stamp,"event":event,"worker_id":worker_id,"session_id":session_id}  
            tuple_line["microtask_id"] = tokens[7]
            tuple_line["file_name"] = tokens[9].strip()
            tuple_line["question"] = self.quote + tokens[11].replace(",",";").replace("\"","\'")  + self.quote
            tuple_line["answer"] = tokens[13].replace(";","_").replace("n\'t","_not_")
            tuple_line["answer_index"] = 0 #this is updated later on after eliminating duplicates
            tuple_line["duration"] = tokens[15]
            index = line.find("explanation%") + "explanation%".__len__()
            tuple_line["explanation"] = self.quote + line[index:].replace(",",";").replace("\"","\'") + self.quote          
        return (tuple_line)
        
    
    def initialize_empty_fields(self):
        '''
        Initialize consent log empty fields to guarantee that columns are aligned,
         even when there is missing data
        '''
        tuple_line={"time_stamp": "",
                    "event":"",     
                    "worker_id":"",
                    "consent_date":"",
                    "test1":"",
                    "test2":"",
                    "test3":"",
                    "test4":"",
                    "qualification_score":"",
                    "test_duration":"",
                    "feedback":"",
                    "gender":"",
                    "years_programming":"",
                    "difficulty":"",
                    "country":"",
                    "age":""
        }
        return(tuple_line)
        
class Parser_Run1(Parser):
    '''
    Parser for the run 1 of experiment 1
    '''
    suffix = "1"
    file_name = "Experiment_1"
    
    def __init__(self,suffix,separator1,separator2):
        '''
        Constructor
        '''
        super().__init__(suffix,separator1,separator2)
        
        '''Dictionary is workerID:sessionID : last number of answer added
        This is used to populate the field that tells the order of the answers (answerOrder)
        '''
        self.answerIndex_map = {"0:0":1} 
        
    def parse_consent_line_to_dictionary(self,line):
        """parse the line into a dictionary"""
        tokens = re.split(self.separator1,line)    
        tuple_line = self.initialize_empty_fields()
        worker_id = re.split(self.separator2,tokens[1])[1].strip()+"_"+self.suffix
        event = tokens[0].rsplit(self.separator2)[1].strip()
        
        '''Capture TimeStamp'''
        time_stamp_event = tokens[0]
        time_stamp = time_stamp_event[:23]
        tuple_line["time_stamp"] = time_stamp
        tuple_line["event"] = event
        tuple_line["worker_id"] = worker_id
 
        if(event=="CONSENT"):   
            tuple_line["consent_date"] = (re.split(self.separator2,tokens[2])[1]).strip()
        elif(event=="SKILLTEST"):
            tuple_line["test1"] = Parser.convert_to_numeric(self,re.split(self.separator2,tokens[2])[1])
            tuple_line["test2"] = Parser.convert_to_numeric(self,re.split(self.separator2,tokens[3])[1])
            tuple_line["test3"] = Parser.convert_to_numeric(self,re.split(self.separator2,tokens[4])[1])
            tuple_line["test4"] = Parser.convert_to_numeric(self,re.split(self.separator2,tokens[5])[1])
            tuple_line["qualification_score"] =  re.split(self.separator2,tokens[6])[1]
            tuple_line["test_duration"] = (re.split(self.separator2,tokens[7])[1]).strip()
        elif(event=="SURVEY"):
            tcount = 3
            results = self.extract_feedback(tokens,3,"Gender=",self.separator2)
            tuple_line["feedback"] = self.quote + results[0].replace("\"","\'")  + self.quote
            tcount = results[1] + 1 
            tuple_line["gender"] = re.split(self.separator2,tokens[tcount])[1].replace(" ","_")
            tcount += 1
            tuple_line["years_programming"] = re.split(self.separator2,tokens[tcount])[1]
            tcount += 1
            tuple_line["difficulty"] = re.split(self.separator2,tokens[tcount])[1] 
            tcount += 1
            tuple_line["country"] = self.quote + re.split(self.separator2,tokens[tcount])[1] + self.quote  
            tcount += 1
            tuple_line["age"] = re.split(self.separator2,tokens[tcount])[1]
        return (tuple_line)     
    
    def initialize_empty_fields(self):
        '''
        Initialize consent log empty fields to guarantee that columns are aligned,
         even when there is missing data
        '''
        tuple_line={"time_stamp": "",
                    "event":"",     
                    "worker_id":"",
                    "consent_date":"",
                    "test1":"",
                    "test2":"",
                    "test3":"",
                    "test4":"",
                    "qualification_score":"",
                    "test_duration":"",
                    "feedback":"",
                    "gender":"",
                    "years_programming":"",
                    "difficulty":"",
                    "country":"",
                    "age":""
        }
        return(tuple_line)
 
    
    def extract_feedback(self,tokens,index,endToken,separator):
        """extracts the feedback text and returns next token position """
        feedback = re.split(separator,tokens[index])[1].replace(",",";")
        index += 1
        while (index < tokens.__len__() and tokens[index].find(endToken)<0): #means that did not find the next valid token yet
            feedback = feedback +" " + tokens[index].replace(",",";")
            index += 1
        results=[feedback,index-1]
        return (results)    
    
    def parse_session_line_to_dictionary(self,line):
        """parse the line into a dictionary"""
        tuple_line = {}
        tokens = re.split(self.separator1,line)    
        time_stamp_event = tokens[0]
        event = re.split(self.separator2,tokens[0])[1]
        time_stamp = time_stamp_event[:23]
        if(event=="MICROTASK"):#Ignore other events
            tuple_line["time_stamp"] = time_stamp
            tuple_line["event"] = event
            worker_id = re.split(self.separator2,tokens[1])[1]+"_"+self.suffix
            session_id = re.split(self.separator2,tokens[2])[1]
            tuple_line["worker_id"] = worker_id
            tuple_line["session_id"] = session_id
            tuple_line["microtask_id"] = re.split(self.separator2,tokens[3])[1]
            tuple_line["file_name"] = re.split(self.separator2,tokens[4])[1].strip()
            tuple_line["question"] = self.quote + re.split(self.separator2,tokens[5])[1].replace(",",";").replace("\"","\'") + self.quote
            tuple_line["answer"] = re.split(self.separator2,tokens[6])[1]
            tuple_line["answer_index"] = 0 #this is updated later on after eliminating duplicates
            tuple_line["duration"] =  re.split(self.separator2,tokens[7])[1]
            position = line.index("explanation=") + "explanation=".__len__()
            tuple_line["explanation"] = self.quote + line[position:].replace(",",";").replace("\"","\'") + self.quote  
        return (tuple_line)
       

    