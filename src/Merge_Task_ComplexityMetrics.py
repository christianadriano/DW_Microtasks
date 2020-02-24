'''
Created on Oct 15, 2019

Extract metrics from a file and append to each microtask line.
The metrics correspond to file (e.g., HIT01_8) and to each program statement)
There are four metrics: LOC, Cyclomatic complexity, Size Char, Halstead Length, Halstead Volume


@author: Christian
'''
import pandas as pd
import arff as arf
import numpy as np

class Merge_Task_ComplexityMetrics(object):
    '''
    classdocs
    '''
    def _load_E2_files(self):
        '''
        load complexity metrics file into a dataframe
        Load task outcomes file into a dataframe
        '''
        
        #TASKS
        dataset_tasks_E2 = arf.loads(open(self.file_tasks_E2, 'rt'))
        array_tasks_E2 = np.array(dataset_tasks_E2['data'])
        self.df_tasks_E2 = pd.DataFrame(array_tasks_E2)
        #print(dataset_tasks_E2['attributes'])
        #need to extract the header, because the arf.loads brings only data....        
        tasks_E2_header = np.take(dataset_tasks_E2['attributes'], [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62])
        self.df_tasks_E2.columns = tasks_E2_header
        
        #COMPLEXITY METRICS
        self.df_complexity_E2 = pd.read_csv(self.file_complexity_E2)


    def _left_join_task_complexity_E2(self):
        '''
        do a left join of the tasks with their corresponding complexity metrics
        for experiment 2
        '''
        self.df_complexity_E2 = self.df_complexity_E2.drop(['file_name', 'type'],axis=1) 
        self.df_tasks_E2['microtask_id'] = self.df_tasks_E2['microtask_id'].astype(int)
        df_results_E2 =pd.merge(self.df_tasks_E2, 
                        self.df_complexity_E2, 
                        on=['microtask_id'], 
                        how='left') 
        print (df_results_E2)
        df_results_E2.to_csv(self.complexity_file_path + 'merged_tasks_complexity_E2.csv')

    def _append_metrics_E1(self):
        '''
        append metrics for experiment 2 tasks
        '''


        
    def __init__(self):
        '''
        Initialize folders 
        '''
        super().__init__()
        task_file_path ='C://Users//Christian//Documents//GitHub//DW_Microtasks//output//'
        self.file_tasks_E2 = task_file_path + 'consolidated_Final_Experiment_2.arff'
        self.file_tasks_E1 = task_file_path + 'consolidated_Final_Experiment_1.arff'
        
        self.complexity_file_path = 'C://Users//Christian//Documents//GitHub//Complexity_Metrics//output//'
        self.file_complexity_E2 = self.complexity_file_path + 'microtask_complexity_E2.csv'
        self.file_complexity_E1 = self.complexity_file_path + 'microtask_complexity_E1.csv'
        
#CONTROLLER CODE
merger = Merge_Task_ComplexityMetrics()
merger._load_E2_files()   
merger._left_join_task_complexity_E2()
