'''
Created on Mar 25, 2018

@author: Christian Adriano
'''

class FileReaderWriter(object):
    '''
    utility functions to reads and writes to an ARFF file
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def write_session_log_arff(self,tuple_lines,output_file_path,header_lines):
        """write the content to an arff file"""
        with open(output_file_path, 'a') as the_file:
            for line in header_lines:     
                the_file.write(line)
                the_file.write("\n")
            for line in tuple_lines:
                the_file.write(self.convert_to_comma_separated(line))
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