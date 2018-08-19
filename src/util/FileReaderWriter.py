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
            """Write header"""
            for line in header_lines:     
                the_file.write(line)
                the_file.write("\n")
            """Write microtask outcomes"""
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
    
