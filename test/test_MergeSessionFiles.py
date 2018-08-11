'''
Created on Mar 20, 2018

@author: Chris
'''
import unittest
from MergeSessionFiles import SessionLoader

class Test(unittest.TestCase):

    def disabled_test_load_file(self):
        self.sessionLoader = SessionLoader()
        file_path = "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData.txt"
        file_lines = self.sessionLoader.load_file(file_path)
        print(file_lines)
        print("eeeeee")
        self.assertEqual(4,file_lines.__len__())

    def disabled_test_consolidate_lines(self):
        self.sessionLoader = SessionLoader()
        file_path = "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData.txt"
        file_set = self.sessionLoader.load_file(file_path)
        file_set = self.sessionLoader.consolidate_broken_lines(file_set[:])
        print(file_set)
        self.assertEqual(3,file_set.__len__())
        
    def disabled_test_parse_line_to_dictionary_OpenSession(self):
        self.sessionLoader = SessionLoader()
        line = "09:04:22.161 [http-bio-8080-exec-5912] INFO  - EVENT=OPEN SESSION; workerId=3; sessionId=499ce8E5e199"
        tuple = self.sessionLoader.parse_line_to_dictionary(line,"1")
        print(tuple)
        self.assertEqual(4,tuple.__len__())

    def disabled_test_parse_line_to_dictionary_Microtask(self):
        self.sessionLoader = SessionLoader()
        line = "09:09:15.319 [http-bio-8080-exec-5909] INFO  - EVENT=MICROTASK; workerId=8; sessionId=498Cg-9e-1g-1-2-9; microtaskId=152; fileName=8buggy_AbstractReviewSection_buggy.txt; question=Is there maybe something wrong in the declaration of function 'appendMessage' at line 78 (e.g., requires a parameter that is not listed, needs different parameters to produce the correct result, specifies the wrong or no return type, etc .)?; answer=PROBABLY_YES; duration=144476.0; explanation=public class IOGraphic { private static StringBuffer sb = new StringBuffer()"
        tuple = self.sessionLoader.parse_line_to_dictionary(line,"1")
        #print(tuple)
        self.assertEqual(10,tuple.__len__())
        
    def disabled_test_parse_all_to_dictionary_Microtask(self):
        self.sessionLoader = SessionLoader()
        file_lines= ["09:04:22.161 [http-bio-8080-exec-5912] INFO  - EVENT=OPEN SESSION; workerId=3; sessionId=499ce8E5e199",
                     "09:09:15.319 [http-bio-8080-exec-5909] INFO  - EVENT=MICROTASK; workerId=8; sessionId=498Cg-9e-1g-1-2-9; microtaskId=152; fileName=8buggy_AbstractReviewSection_buggy.txt; question=Is there maybe something wrong in the declaration of function 'appendMessage' at line 78 (e.g., requires a parameter that is not listed, needs different parameters to produce the correct result, specifies the wrong or no return type, etc .)?; answer=PROBABLY_YES; duration=144476.0; explanation=public class IOGraphic { private static StringBuffer sb = new StringBuffer()",
                     "09:09:23.327 [http-bio-8080-exec-5933] INFO  - EVENT=CLOSE SESSION; workerId=64; sessionId=493aC-4e0g-2-3-9"
                     ]
        file_lines_tuples = self.sessionLoader.parse_all_to_dictionary(file_lines, "1")
        self.assertEqual(4,file_lines_tuples[0].__len__())   
        self.assertEqual(10,file_lines_tuples[1].__len__())  
        self.assertEqual(4,file_lines_tuples[2].__len__()) 
 
    def test_match_start_tuple(self):
        self.sessionLoader = SessionLoader()
        match_result = self.sessionLoader.match_start_tuple("01:04:01")
        self.assertTrue(match_result, "matching start did not work!")
        print(match_result)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()