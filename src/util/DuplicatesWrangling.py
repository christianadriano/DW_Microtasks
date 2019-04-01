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
        i=0
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
    
    def process_duplicates(self, tuples):
        '''
        identifies and counts the duplicate items
        remove them returning a new tuple list without duplicates
        '''
        duplicate_tuples = self.count_duplicates_E1(tuples)
        processed_tuples = self.remove_duplicates(tuples, duplicate_tuples) 
        return (processed_tuples)

    def test_duplicate_removal(self):
        tuples = self.load_tuples()
        duplicate_map = self.count_duplicates_E1(tuples) 
        tuples = self.remove_duplicates(tuples,duplicate_map)
            
        print("after duplicate removal = "+ str(len(tuples)))
        ''' recounting to confirm removals ''' 
        duplicate_map = self.count_duplicates_E1(tuples) 
        print(duplicate_map)

dup = DuplicatesWrangling()
dup.test_duplicate_removal()
