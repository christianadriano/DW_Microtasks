'''
Created on Mar 20, 2018

@author: Chris
'''
import unittest
from MergeSessionFiles import SessionLoader

class Test(unittest.TestCase):

    def ttest_load_file(self):
        self.sessionLoader = SessionLoader()
        file_path = "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData.txt"
        file_lines = self.sessionLoader.load_file(file_path)
        #print(file_lines)
        self.assertEqual(4,file_lines.__len__())

    def test_consolidate_lines(self):
        self.sessionLoader = SessionLoader()
        file_path = "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData.txt"
        file_set = self.sessionLoader.load_file(file_path)
        file_set = self.sessionLoader.consolidate_broken_lines(file_set[:])
        print(file_set)
        self.assertEqual(3,file_set.__len__())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()