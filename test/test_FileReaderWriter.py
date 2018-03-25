'''
Created on Mar 25, 2018

@author: Chris
'''
import unittest
from util.FileReaderWriter import FileReaderWriter 


class Test(unittest.TestCase):


    def test_write_to_file(self):
        self.fileReaderWriter = FileReaderWriter()
        tuple_lines= [{"time-stamp":"09:04:22.161","EVENT":"OPEN SESSION","worker_id":"3","session_id":"499ce8E5e199"}]
                     #"09:09:15.319 [http-bio-8080-exec-5909] INFO  - EVENT=MICROTASK; workerId=8; sessionId=498Cg-9e-1g-1-2-9; microtaskId=152; fileName=8buggy_AbstractReviewSection_buggy.txt; question=Is there maybe something wrong in the declaration of function 'appendMessage' at line 78 (e.g., requires a parameter that is not listed, needs different parameters to produce the correct result, specifies the wrong or no return type, etc .)?; answer=PROBABLY_YES; duration=144476.0; explanation=public class IOGraphic { private static StringBuffer sb = new StringBuffer()",
                     #"09:09:23.327 [http-bio-8080-exec-5933] INFO  - EVENT=CLOSE SESSION; workerId=64; sessionId=493aC-4e0g-2-3-9"
                     #]
                     
        header_lines=["% 1. Title: First Failure Understanding Database",
                    "%" ,
                    "% 2. Sources:",
                    "%      (a) Creator: Christian Medeiros Adriano",
                    "%      (b) Date: March, 2018",
                    "%"
                    ]
        file_lines_tuples = self.fileReaderWriter.write_session_log_arff(tuple_lines, 
                                                                      "test_output_file.txt",
                                                                      header_lines
                                                                      )



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    