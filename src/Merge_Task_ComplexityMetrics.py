'''
Created on Oct 15, 2019

Extract metrics from a file and append to each microtask line.
The metrics correspond to file (e.g., HIT01_8) and to each program statement)
There are four metrics: LOC, Cyclomatic complexity, Size Char, Halstead Length, Halstead Volume


@author: Christian
'''
from scipy.io import arff
import pandas as pd

class Merge_Task_ComplexityMetrics(object):
    '''
    classdocs
    '''
    def _load_E2_files(self):
        '''
        load complexity metrics file into a dataframe
        Load task outcomes file into a dataframe
        '''
        
        array_tasks_E2=pd.arff.loadarff(self.file_tasks_E2)
        df_tasks_E2 = pd.DataFrame(array_tasks_E2[0])
        df_complexity = pd.read_csv(self.file_tasks_E2)

    def _append_metrics_E2(self):
        '''
        append metrics for experiment 2 tasks
        '''

    def _append_metrics_E1(self):
        '''
        append metrics for experiment 2 tasks
        '''


        
    def __init__(self):
        '''
        Initialize folders 
        '''
        super().__init__()
        self.file_root ='C://Users//Christian//Documents//GitHub//DW_Microtasks//output//'
        self.file_tasks_E2 = file_root + 'consolidated_Final_Experiment_2.arff'
        self.file_tasks_E1 = file_root + 'consolidated_Final_Experiment_1.arff'
        self.file_complexity_E2 = file_root + ''
        self.file_complexity_E1 =''
        
        
        '''self.file_testInput = 'C://Users//Christian//Documents//GitHub//DW_Microtasks//test//'        
        
        