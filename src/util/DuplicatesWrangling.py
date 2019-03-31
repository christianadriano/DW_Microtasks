'''
Created on Mar 31, 2019

Count the number of duplicates according to a rule
Remove duplicates according to a rule

@author: Christian
'''

from Merge_Files import Merge_Files
from parserFactory import Parser

class DuplicatesWrangling(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.merger = Merge_Files()
        self.root = 'C://Users//Christian//Dropbox (Personal)//FaultLocalization_Microtasks_data//Experiment-1_2014//'
    
    def load_tuples(self):
        tuple_lines = self.merger.run(
                               self.root + "session_Run1-Total-25oct.log",
                               self.root + "consent_Run1-Total-25oct.log",
                               #self.testInput + "sessionTestData.txt",
                               #self.testInput + "consentTestData.txt",
                                Parser.Parser.factory_method(self,worker_id_suffix='1', separator1=";", separator2="=")
                               ) 
        print("tuple_lines = "+ str(len(tuple_lines)))
        return tuple_lines
        
    def count_duplicates_E1(self,tuples):
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

            
        print("Duplicated items:")
        print(duplicate_map)    
        
dup = DuplicatesWrangling()
dup.count_duplicates_E1(dup.load_tuples()) 
        