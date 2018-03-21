'''
Created on Mar 20, 2018

@author: Chris
'''
import unittest
from MergeSessionFiles import SessionLoader

class Test(unittest.TestCase):

    def test_load_file(self):
        self.sessionLoader = SessionLoader()
        file_path = "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData.txt"
        file_lines = self.sessionLoader.load_file(file_path)
        print(file_lines)
        self.assertEqual(4,file_lines.__len__())

    def consolidate_lines(self):
        self.sessionLoader = SessionLoader()
        file_path = "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData.txt"
        file_lines = self.sessionLoader.load_file(file_path)
        file_lines = self.sessionLoader.consolidate_broken_explanations(file_lines)
        print(file_lines)
        self.assertEqual(3,file_lines.__len__())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()